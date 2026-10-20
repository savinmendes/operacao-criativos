"""Helper de requisição HTTP com retry/backoff exponencial.

Compartilhado pelos três clients de API (fal.ai, ElevenLabs, HeyGen) para não
duplicar a mesma lógica de rate limit / timeout três vezes.
"""

from __future__ import annotations

import random
import time
from typing import Any

import requests


class ApiError(RuntimeError):
    """Erro de API após esgotar as tentativas de retry."""


def request_with_retry(
    method: str,
    url: str,
    *,
    max_retries: int = 5,
    base_delay: float = 1.0,
    timeout: float = 60.0,
    **kwargs: Any,
) -> requests.Response:
    """Faz uma requisição HTTP com retry exponencial para rate limit e timeout.

    Repete em caso de HTTP 429 (respeitando o header `Retry-After` quando
    presente) e em caso de timeout/erro de conexão. Para outros erros HTTP
    (4xx/5xx que não sejam 429), levanta imediatamente — não adianta tentar
    de novo uma requisição malformada.
    """
    ultimo_erro: Exception | None = None

    for tentativa in range(1, max_retries + 1):
        try:
            resposta = requests.request(method, url, timeout=timeout, **kwargs)
        except (requests.ConnectionError, requests.Timeout) as exc:
            ultimo_erro = exc
            if tentativa == max_retries:
                break
            _esperar(base_delay, tentativa)
            continue

        if resposta.status_code == 429:
            ultimo_erro = ApiError(f"Rate limit (429) em {url}")
            if tentativa == max_retries:
                break
            retry_after = resposta.headers.get("Retry-After")
            espera = float(retry_after) if retry_after else _delay_exponencial(base_delay, tentativa)
            time.sleep(espera)
            continue

        if resposta.status_code >= 500:
            ultimo_erro = ApiError(f"Erro de servidor ({resposta.status_code}) em {url}")
            if tentativa == max_retries:
                break
            _esperar(base_delay, tentativa)
            continue

        return resposta

    raise ApiError(
        f"Falha ao chamar {url} após {max_retries} tentativas: {ultimo_erro}"
    ) from ultimo_erro


def _delay_exponencial(base_delay: float, tentativa: int) -> float:
    jitter = random.uniform(0, base_delay * 0.5)
    return base_delay * (2 ** (tentativa - 1)) + jitter


def _esperar(base_delay: float, tentativa: int) -> None:
    time.sleep(_delay_exponencial(base_delay, tentativa))

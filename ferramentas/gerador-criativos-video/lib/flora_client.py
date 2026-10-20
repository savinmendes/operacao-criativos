"""Client genérico para rodar "techniques" (workflows salvos no canvas) da Flora AI.

A API da Flora não tem endpoints fixos de "gerar vídeo"/"gerar imagem" como o
fal.ai — ela executa um workflow (technique) que você monta e salva no canvas
em app.flora.ai. Este client é genérico: você fornece o `technique_id` (ou
slug) e o dicionário de `inputs` que aquela technique espera.

Referência (pesquisada em set/2026): https://developer.flora.ai/reference/
- Rodar:            POST https://app.flora.ai/api/v1/techniques/{technique_id}/runs
- Status/resultado: GET  https://app.flora.ai/api/v1/techniques/{technique_id}/runs/{run_id}
"""

from __future__ import annotations

import time

import config
from lib.retry import ApiError, request_with_retry

API_BASE_URL = "https://app.flora.ai/api/v1"

POLL_INTERVALO_SEGUNDOS = 5.0
POLL_TIMEOUT_SEGUNDOS = 600.0


def _headers() -> dict[str, str]:
    chave = config.require(config.FLORA_API_KEY, "FLORA_API_KEY")
    return {
        "Authorization": f"Bearer {chave}",
        "Content-Type": "application/json",
    }


def run_technique(technique_id: str, inputs: dict) -> str:
    """Submete uma execução de uma technique salva no canvas da Flora.

    Args:
        technique_id: ID (ou slug) da technique, visível na página dela no canvas.
        inputs: dicionário com os parâmetros de entrada que a technique espera
            (varia por technique — confira o schema dela em app.flora.ai).

    Returns:
        runId da execução, usado em poll_run para acompanhar o progresso.
    """
    resposta = request_with_retry(
        "POST",
        f"{API_BASE_URL}/techniques/{technique_id}/runs",
        headers=_headers(),
        json={"inputs": inputs},
    )
    dados = resposta.json()
    run_id = dados.get("runId")
    if not run_id:
        raise ApiError(f"Resposta da Flora sem runId: {dados}")
    return run_id


def poll_run(technique_id: str, run_id: str) -> list[dict]:
    """Aguarda a conclusão de uma execução e retorna a lista de outputs.

    Args:
        technique_id: mesmo ID usado em run_technique.
        run_id: retornado por run_technique.

    Returns:
        Lista de outputs, cada um no formato `{"outputId", "type", "url"}`.
    """
    inicio = time.monotonic()
    url_status = f"{API_BASE_URL}/techniques/{technique_id}/runs/{run_id}"

    while True:
        resposta = request_with_retry("GET", url_status, headers=_headers())
        dados = resposta.json()
        status = dados.get("status")

        if status == "completed":
            outputs = dados.get("outputs")
            if not outputs:
                raise ApiError(f"Flora marcou run {run_id} como completo sem outputs: {dados}")
            return outputs

        if status == "failed":
            raise ApiError(f"Execução {run_id} falhou na Flora: {dados}")

        if time.monotonic() - inicio > POLL_TIMEOUT_SEGUNDOS:
            raise ApiError(
                f"Timeout esperando conclusão da execução {run_id} (último status: {status})"
            )

        time.sleep(POLL_INTERVALO_SEGUNDOS)


def generate(technique_id: str, inputs: dict) -> str:
    """Atalho: roda a technique, aguarda conclusão e retorna a URL do primeiro output.

    Para técnicas com múltiplos outputs, use run_technique + poll_run
    diretamente e percorra a lista completa.
    """
    run_id = run_technique(technique_id, inputs)
    outputs = poll_run(technique_id, run_id)
    primeira_url = outputs[0].get("url")
    if not primeira_url:
        raise ApiError(f"Primeiro output da execução {run_id} sem URL: {outputs[0]}")
    return primeira_url

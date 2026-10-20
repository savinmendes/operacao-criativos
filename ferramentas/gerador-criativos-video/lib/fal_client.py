"""Client para geração de vídeo/imagem via fal.ai (API de fila assíncrona).

Referência: https://docs.fal.ai/model-apis/model-endpoints/queue
- Submit: POST https://queue.fal.run/{model} → retorna status_url/response_url
  próprios da requisição (IMPORTANTE: não é {model}/requests/{id}/status — o
  prefixo real costuma ser só o "app id", ex. fal-ai/bytedance, não o caminho
  completo do modelo como fal-ai/bytedance/seedance/v1.5/pro/text-to-video.
  Por isso o polling usa sempre as URLs devolvidas pelo submit, nunca
  reconstruídas a partir do nome do modelo).
"""

from __future__ import annotations

import time

import config
from lib.retry import ApiError, request_with_retry

QUEUE_BASE_URL = "https://queue.fal.run"

# Seedance 2.5 e Flux 2 Pro (pedido original) — endpoint id confirmado direto
# na doc do fal.ai em set/2026, não é o mesmo formato de caminho do v1.x.
MODELO_VIDEO_PADRAO = "bytedance/seedance-2.5/text-to-video"
MODELO_IMAGEM_PADRAO = "fal-ai/flux-2-pro"

RESOLUCOES_IMAGEM_POR_ASPECT_RATIO = {
    "9:16": {"width": 720, "height": 1280},
    "16:9": {"width": 1280, "height": 720},
    "1:1": {"width": 1080, "height": 1080},
}

POLL_INTERVALO_SEGUNDOS = 5.0
POLL_TIMEOUT_SEGUNDOS = 600.0


def _headers() -> dict[str, str]:
    chave = config.require(config.FAL_KEY, "FAL_KEY")
    return {
        "Authorization": f"Key {chave}",
        "Content-Type": "application/json",
    }


def _submeter(modelo: str, payload: dict) -> dict:
    """Envia um job para a fila do fal.ai e retorna a resposta completa da submissão
    (contém request_id, status_url e response_url — usados no polling a seguir).
    """
    resposta = request_with_retry(
        "POST",
        f"{QUEUE_BASE_URL}/{modelo}",
        headers=_headers(),
        json=payload,
    )
    dados = resposta.json()
    if not dados.get("request_id") or not dados.get("status_url") or not dados.get("response_url"):
        raise ApiError(f"Resposta do fal.ai incompleta (sem request_id/status_url/response_url): {dados}")
    return dados


def _aguardar_conclusao(dados_submissao: dict) -> dict:
    """Faz polling do status (usando as URLs devolvidas pelo submit) até COMPLETED."""
    url_status = dados_submissao["status_url"]
    url_resultado = dados_submissao["response_url"]
    request_id = dados_submissao["request_id"]
    inicio = time.monotonic()

    while True:
        resposta = request_with_retry("GET", url_status, headers=_headers())
        status = resposta.json().get("status")

        if status == "COMPLETED":
            resultado = request_with_retry("GET", url_resultado, headers=_headers())
            return resultado.json()

        if time.monotonic() - inicio > POLL_TIMEOUT_SEGUNDOS:
            raise ApiError(
                f"Timeout esperando conclusão do job {request_id} (último status: {status})"
            )

        time.sleep(POLL_INTERVALO_SEGUNDOS)


def generate_video(
    prompt: str,
    model: str = MODELO_VIDEO_PADRAO,
    duration: int = 5,
    aspect_ratio: str = "9:16",
    resolution: str = "1080p",
    generate_audio: bool = False,
    bitrate_mode: str = "high",
) -> str:
    """Gera um vídeo a partir de um prompt de texto e retorna a URL do resultado.

    Args:
        prompt: descrição da cena a ser gerada.
        model: identificador do modelo no fal.ai.
        duration: duração desejada em segundos. O Seedance 2.5 aceita de 4 a
            30 — valores fora disso são arredondados e limitados a essa faixa
            antes de enviar. Se você precisa de um clipe mais curto que 4s
            (ex.: para um cutaway), gere no mínimo permitido e corte o
            excedente depois com ffmpeg — é o que
            `lib/ffmpeg_merge.build_avatar_with_cutaways` já faz automaticamente.
        aspect_ratio: proporção do vídeo — "9:16", "16:9", "1:1", "4:3", "3:4"
            ou "21:9" (o Seedance 2.5 aceita esses valores direto, sem
            precisar de width/height).
        resolution: "480p", "720p" ou "1080p". Padrão 1080p — o Seedance 2.5
            suporta bem essa resolução e a diferença de qualidade é grande
            pra um criativo de anúncio.
        generate_audio: se o modelo deve gerar áudio nativo junto. Padrão False —
            o áudio do criativo vem do ElevenLabs, e desligar aqui corta o custo.
        bitrate_mode: "standard" ou "high". Padrão "high" — evita comprimir o
            clipe de origem mais do que o necessário antes mesmo de chegar
            no nosso re-encode.

    Returns:
        URL pública do vídeo gerado.
    """
    duracao_valida = max(4, min(30, round(duration)))
    payload = {
        "prompt": prompt,
        "duration": str(duracao_valida),
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "generate_audio": generate_audio,
        "bitrate_mode": bitrate_mode,
    }
    dados_submissao = _submeter(model, payload)
    resultado = _aguardar_conclusao(dados_submissao)

    video = resultado.get("video")
    if not video or not video.get("url"):
        raise ApiError(f"Resposta do fal.ai sem vídeo: {resultado}")
    return video["url"]


def generate_image(
    prompt: str,
    model: str = MODELO_IMAGEM_PADRAO,
    aspect_ratio: str = "9:16",
) -> str:
    """Gera uma imagem a partir de um prompt de texto e retorna a URL do resultado.

    Args:
        prompt: descrição da imagem a ser gerada.
        model: identificador do modelo no fal.ai (ex.: fal-ai/flux-2-pro).
        aspect_ratio: "9:16", "16:9" ou "1:1". O Flux 2 Pro não tem um campo
            "aspect_ratio" direto — usa `image_size` com width/height
            explícitos, traduzido aqui a partir desse parâmetro. Sem isso, o
            Flux gera em formato quadrado por padrão (bug real encontrado: a
            imagem do avatar saiu quadrada porque essa tradução não existia).

    Returns:
        URL pública da imagem gerada.
    """
    tamanho = RESOLUCOES_IMAGEM_POR_ASPECT_RATIO.get(aspect_ratio, RESOLUCOES_IMAGEM_POR_ASPECT_RATIO["9:16"])
    payload = {"prompt": prompt, "image_size": tamanho}
    dados_submissao = _submeter(model, payload)
    resultado = _aguardar_conclusao(dados_submissao)

    imagens = resultado.get("images")
    if not imagens or not imagens[0].get("url"):
        raise ApiError(f"Resposta do fal.ai sem imagem: {resultado}")
    return imagens[0]["url"]

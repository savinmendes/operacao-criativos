"""Client para avatar falando com lip-sync via HeyGen (API v2).

Referências (pesquisadas em set/2026 — a API da HeyGen está em transição para
uma v3; ver nota no README se algo aqui parar de funcionar):
- Upload de asset genérico (áudio):  POST https://api.heygen.com/v3/assets
- Upload de talking photo (imagem):  POST https://upload.heygen.com/v1/talking_photo
  IMPORTANTE: o asset_id do upload genérico NÃO funciona como talking_photo_id —
  a HeyGen exige esse endpoint dedicado pra imagem virar um "avatar/look"
  utilizável (erro real observado ao tentar usar asset_id genérico:
  "avatar look not found"). Corpo é o binário puro da imagem, não multipart.
- Gerar vídeo:      POST https://api.heygen.com/v2/video/generate
- Status do vídeo:  GET  https://api.heygen.com/v1/video_status.get?video_id=...
"""

from __future__ import annotations

import mimetypes
import os
import time

import config
from lib.retry import ApiError, request_with_retry

ASSETS_URL = "https://api.heygen.com/v3/assets"
TALKING_PHOTO_UPLOAD_URL = "https://upload.heygen.com/v1/talking_photo"
GENERATE_URL = "https://api.heygen.com/v2/video/generate"
STATUS_URL = "https://api.heygen.com/v1/video_status.get"

POLL_INTERVALO_SEGUNDOS = 8.0
POLL_TIMEOUT_SEGUNDOS = 900.0

# Mapeia aspect_ratio -> dimensão em pixels enviada pra HeyGen.
DIMENSOES_POR_ASPECT_RATIO = {
    "9:16": {"width": 720, "height": 1280},
    "16:9": {"width": 1280, "height": 720},
    "1:1": {"width": 1080, "height": 1080},
}


def _headers(content_type: str | None = "application/json") -> dict[str, str]:
    chave = config.require(config.HEYGEN_API_KEY, "HEYGEN_API_KEY")
    headers = {"X-Api-Key": chave}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def _extrair_dados(resposta_json: dict) -> dict:
    """Extrai o campo 'data' de uma resposta da HeyGen.

    A HeyGen retorna `data: null` + um campo `error` (ex.: `insufficient_credit`)
    quando algo dá errado, mesmo com HTTP 402/400 — sem checar isso aqui, o
    código quebraria com um AttributeError genérico ('NoneType' has no 'get')
    em vez de mostrar o motivo real do erro.
    """
    erro = resposta_json.get("error")
    if erro:
        raise ApiError(f"Erro da HeyGen ({erro.get('code')}): {erro.get('message')}")
    dados = resposta_json.get("data")
    if not dados:
        raise ApiError(f"Resposta da HeyGen sem 'data': {resposta_json}")
    return dados


def upload_asset(file_path: str) -> str:
    """Faz upload de um arquivo local (imagem ou áudio) e retorna o asset_id.

    Args:
        file_path: caminho local do arquivo (imagem .jpg/.png ou áudio .mp3/.wav).

    Returns:
        asset_id gerado pela HeyGen, usado depois em create_avatar_video.
    """
    if not os.path.isfile(file_path):
        raise ApiError(f"Arquivo não encontrado para upload: {file_path}")

    with open(file_path, "rb") as arquivo:
        resposta = request_with_retry(
            "POST",
            ASSETS_URL,
            headers=_headers(content_type=None),
            files={"file": arquivo},
        )

    dados = _extrair_dados(resposta.json())
    asset_id = dados.get("asset_id")
    if not asset_id:
        raise ApiError(f"Resposta da HeyGen sem asset_id: {dados}")
    return asset_id


def upload_talking_photo(file_path: str) -> str:
    """Faz upload de uma imagem local pelo endpoint dedicado de talking photo
    e retorna o talking_photo_id (diferente do asset_id genérico — ver nota
    no topo do arquivo).

    Args:
        file_path: caminho local da imagem (.jpg/.jpeg/.png).

    Returns:
        talking_photo_id, usado em create_avatar_video.
    """
    if not os.path.isfile(file_path):
        raise ApiError(f"Arquivo não encontrado para upload: {file_path}")

    content_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"

    with open(file_path, "rb") as arquivo:
        resposta = request_with_retry(
            "POST",
            TALKING_PHOTO_UPLOAD_URL,
            headers=_headers(content_type=content_type),
            data=arquivo.read(),
        )

    dados = _extrair_dados(resposta.json())
    talking_photo_id = dados.get("talking_photo_id")
    if not talking_photo_id:
        raise ApiError(f"Resposta da HeyGen sem talking_photo_id: {dados}")
    return talking_photo_id


def _resolver_asset_id(caminho_local_ou_asset_id: str) -> str:
    """Se receber um caminho de arquivo local existente, faz upload (endpoint
    genérico de asset) e retorna o asset_id gerado; caso contrário, assume que
    o valor já é um asset_id da HeyGen (uso avançado/manual) e o retorna sem
    alteração. Usado só pro áudio — para imagem, ver _resolver_talking_photo_id.
    """
    if os.path.isfile(caminho_local_ou_asset_id):
        return upload_asset(caminho_local_ou_asset_id)
    return caminho_local_ou_asset_id


def _resolver_talking_photo_id(caminho_local_ou_id: str) -> str:
    """Se receber um caminho de arquivo local existente, faz upload pelo
    endpoint dedicado de talking photo; caso contrário, assume que o valor já
    é um talking_photo_id da HeyGen (uso avançado/manual) e o retorna sem
    alteração.
    """
    if os.path.isfile(caminho_local_ou_id):
        return upload_talking_photo(caminho_local_ou_id)
    return caminho_local_ou_id


def create_avatar_video(
    image_url: str,
    audio_url_or_path: str,
    aspect_ratio: str = "9:16",
) -> str:
    """Cria um vídeo de avatar falando com lip-sync a partir de imagem + áudio.

    A HeyGen precisa de IDs próprios (não aceita URL externa arbitrária) — por
    isso, se `image_url` ou `audio_url_or_path` forem caminhos de arquivo
    local existentes, o upload é feito automaticamente antes de gerar o
    vídeo (imagem via endpoint dedicado de talking photo, áudio via endpoint
    genérico de asset — são upload endpoints diferentes). Se a imagem vier de
    uma URL remota (ex.: gerada pelo fal.ai), baixe-a para um arquivo local
    antes de chamar esta função (veja `lib/ffmpeg_merge.baixar_arquivo`).

    Args:
        image_url: caminho local da imagem (ou um talking_photo_id já
            existente na HeyGen, para uso avançado).
        audio_url_or_path: caminho local do áudio .mp3/.wav (ou um
            audio_asset_id já existente na HeyGen).
        aspect_ratio: "9:16", "16:9" ou "1:1".

    Returns:
        video_id do vídeo em geração (usar em poll_video_status para obter a URL final).
    """
    talking_photo_id = _resolver_talking_photo_id(image_url)
    audio_asset_id = _resolver_asset_id(audio_url_or_path)

    dimensao = DIMENSOES_POR_ASPECT_RATIO.get(aspect_ratio, DIMENSOES_POR_ASPECT_RATIO["9:16"])

    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "talking_photo",
                    "talking_photo_id": talking_photo_id,
                    "scale": 1.0,
                },
                "voice": {
                    "type": "audio",
                    "audio_asset_id": audio_asset_id,
                },
                "background": {"type": "color", "value": "#000000"},
            }
        ],
        "dimension": dimensao,
    }

    resposta = request_with_retry("POST", GENERATE_URL, headers=_headers(), json=payload)
    dados = _extrair_dados(resposta.json())
    video_id = dados.get("video_id")
    if not video_id:
        raise ApiError(f"Resposta da HeyGen sem video_id: {dados}")
    return video_id


def poll_video_status(video_id: str) -> str:
    """Aguarda a conclusão do vídeo e retorna a URL final.

    Args:
        video_id: ID retornado por create_avatar_video.

    Returns:
        URL pública do vídeo final (status "completed").
    """
    inicio = time.monotonic()

    while True:
        resposta = request_with_retry(
            "GET",
            STATUS_URL,
            headers=_headers(content_type=None),
            params={"video_id": video_id},
        )
        dados = _extrair_dados(resposta.json())
        status = dados.get("status")

        if status == "completed":
            video_url = dados.get("video_url")
            if not video_url:
                raise ApiError(f"HeyGen marcou vídeo como completo sem video_url: {dados}")
            return video_url

        if status == "failed":
            raise ApiError(f"Geração do vídeo {video_id} falhou na HeyGen: {dados}")

        if time.monotonic() - inicio > POLL_TIMEOUT_SEGUNDOS:
            raise ApiError(
                f"Timeout esperando conclusão do vídeo {video_id} (último status: {status})"
            )

        time.sleep(POLL_INTERVALO_SEGUNDOS)

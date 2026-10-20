"""Client para text-to-speech via ElevenLabs (voz clonada).

Referência: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
"""

from __future__ import annotations

import os

import config
from lib.retry import ApiError, request_with_retry

API_BASE_URL = "https://api.elevenlabs.io/v1"


def generate_speech(
    text: str,
    voice_id: str,
    output_path: str,
    model_id: str = "eleven_multilingual_v2",
) -> str:
    """Gera áudio a partir de texto e salva como um arquivo .mp3 local.

    Args:
        text: texto a ser falado (roteiro da fala).
        voice_id: ID da voz clonada no ElevenLabs.
        output_path: caminho local onde o .mp3 será salvo.
        model_id: modelo de TTS a usar (multilíngue por padrão, cobre espanhol).

    Returns:
        O próprio `output_path`, para encadeamento no pipeline.
    """
    chave = config.require(config.ELEVENLABS_API_KEY, "ELEVENLABS_API_KEY")
    headers = {
        "xi-api-key": chave,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
    }

    resposta = request_with_retry(
        "POST",
        f"{API_BASE_URL}/text-to-speech/{voice_id}",
        headers=headers,
        json=payload,
    )

    if not resposta.content:
        raise ApiError(f"ElevenLabs retornou áudio vazio para voice_id={voice_id}")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as arquivo:
        arquivo.write(resposta.content)

    return output_path

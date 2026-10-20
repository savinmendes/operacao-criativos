"""Carrega configuração do projeto a partir de variáveis de ambiente (.env)."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

FAL_KEY: str | None = os.getenv("FAL_KEY")
ELEVENLABS_API_KEY: str | None = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID: str | None = os.getenv("ELEVENLABS_VOICE_ID")
HEYGEN_API_KEY: str | None = os.getenv("HEYGEN_API_KEY")
FLORA_API_KEY: str | None = os.getenv("FLORA_API_KEY")

# IDs das "techniques" da Flora usadas pelo pipeline principal (main.py) para
# gerar, respectivamente, o vídeo de b-roll e a imagem do avatar. Cada uma é
# montada e salva manualmente no canvas em app.flora.ai — não têm um valor
# padrão possível, precisam ser preenchidas depois que as techniques existirem.
FLORA_TECHNIQUE_ID_VIDEO: str | None = os.getenv("FLORA_TECHNIQUE_ID_VIDEO")
FLORA_TECHNIQUE_ID_IMAGEM: str | None = os.getenv("FLORA_TECHNIQUE_ID_IMAGEM")

# Nome do campo de input que recebe o texto do prompt nas techniques acima.
# Varia por technique — ajuste aqui (ou via .env) se a sua não usar "prompt".
FLORA_PROMPT_INPUT_KEY: str = os.getenv("FLORA_PROMPT_INPUT_KEY", "prompt")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
TMP_DIR = os.path.join(OUTPUT_DIR, "tmp")


def require(value: str | None, nome_variavel: str) -> str:
    """Garante que uma variável de configuração obrigatória está presente.

    Só é chamada na hora de efetivamente usar a chave (não na importação do
    módulo), para que `config.py` possa ser importado mesmo sem `.env`
    preenchido — útil para testes e para os outros módulos carregarem sem
    quebrar antes da primeira chamada de API real.
    """
    if not value:
        raise RuntimeError(
            f"Variável de ambiente '{nome_variavel}' não configurada. "
            f"Copie .env.example para .env e preencha as chaves necessárias."
        )
    return value

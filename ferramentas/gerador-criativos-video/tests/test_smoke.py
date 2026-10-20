"""Teste de fumaça: garante que todos os módulos importam sem erro (mesmo sem
.env preenchido) e que .env.example lista todas as variáveis esperadas.

Rodar com: python -m pytest tests/test_smoke.py -v
ou, sem pytest: python tests/test_smoke.py
"""

from __future__ import annotations

import importlib
import os
import sys

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ_PROJETO not in sys.path:
    sys.path.insert(0, RAIZ_PROJETO)

MODULOS_ESPERADOS = [
    "config",
    "main",
    "lib.retry",
    "lib.fal_client",
    "lib.elevenlabs_client",
    "lib.heygen_client",
    "lib.flora_client",
    "lib.ffmpeg_merge",
]

VARIAVEIS_ESPERADAS_NO_ENV_EXAMPLE = [
    "FAL_KEY",
    "ELEVENLABS_API_KEY",
    "ELEVENLABS_VOICE_ID",
    "HEYGEN_API_KEY",
    "FLORA_API_KEY",
]


def test_todos_os_modulos_importam_sem_erro() -> None:
    for nome_modulo in MODULOS_ESPERADOS:
        importlib.import_module(nome_modulo)


def test_env_example_tem_todas_as_variaveis() -> None:
    caminho_env_example = os.path.join(RAIZ_PROJETO, ".env.example")
    with open(caminho_env_example, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    faltando = [var for var in VARIAVEIS_ESPERADAS_NO_ENV_EXAMPLE if var not in conteudo]
    assert not faltando, f"Variáveis faltando em .env.example: {faltando}"


if __name__ == "__main__":
    test_todos_os_modulos_importam_sem_erro()
    print("OK: todos os módulos importam sem erro.")
    test_env_example_tem_todas_as_variaveis()
    print("OK: .env.example tem todas as variáveis esperadas.")

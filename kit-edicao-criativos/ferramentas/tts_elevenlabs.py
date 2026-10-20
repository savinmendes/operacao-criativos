# -*- coding: utf-8 -*-
"""Narração ElevenLabs direto pela API (sem MCP), já com o alinhamento palavra a palavra
para a legenda sair sincronizada.

Precisa da variável de ambiente ELEVENLABS_API_KEY (ou arquivo .env na raiz do kit).

Vozes salvas (apelido -> voice_id):
  divina   ArTYCGluU0cZhq1bF7Hp   (VOZ DIVINA — San Benito)
  chilena  uHo8F3FY11rc2LxCwDSB   (Chile — desmalezadora)

Exemplos:
  python tts_elevenlabs.py "Esta máquina corta hasta árboles." -o narr.mp3 --voz chilena
  python tts_elevenlabs.py --arquivo roteiro.txt -o narr.mp3 --voz divina
  -> gera narr.mp3 e narr.alinhamento.json (use em: legenda.py narr.mp3 --alinhamento narr.alinhamento.json)

Custo aproximado: ~US$0,165 por 1.000 caracteres (o script mostra antes de gerar; use --sim para pular a pergunta).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests

KIT = Path(__file__).resolve().parent.parent
VOZES = {"divina": "ArTYCGluU0cZhq1bF7Hp", "chilena": "uHo8F3FY11rc2LxCwDSB"}
USD_POR_1000 = 0.165


def chave() -> str:
    k = os.environ.get("ELEVENLABS_API_KEY")
    env = KIT / ".env"
    if not k and env.exists():
        for l in env.read_text(encoding="utf-8").splitlines():
            if l.startswith("ELEVENLABS_API_KEY="):
                k = l.split("=", 1)[1].strip().strip('"')
    if not k:
        raise SystemExit("Defina ELEVENLABS_API_KEY (variável de ambiente ou .env na pasta do kit).")
    return k


def gerar(texto: str, saida: str, voz: str = "divina", modelo: str = "eleven_multilingual_v2",
          estabilidade: float = 0.5, similaridade: float = 0.75, estilo: float = 0.0, velocidade: float = 1.0):
    voice_id = VOZES.get(voz, voz)
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps",
        params={"output_format": "mp3_44100_128"},
        headers={"xi-api-key": chave(), "Content-Type": "application/json"},
        json={"text": texto, "model_id": modelo,
              "voice_settings": {"stability": estabilidade, "similarity_boost": similaridade,
                                 "style": estilo, "use_speaker_boost": True, "speed": velocidade}},
        timeout=300)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:500]}")
    d = r.json()
    Path(saida).write_bytes(base64.b64decode(d["audio_base64"]))
    al = d.get("normalized_alignment") or d.get("alignment")
    jp = str(Path(saida).with_suffix("")) + ".alinhamento.json"
    Path(jp).write_text(json.dumps(al, ensure_ascii=False), encoding="utf-8")
    return saida, jp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texto", nargs="?")
    ap.add_argument("--arquivo", help="txt com o roteiro")
    ap.add_argument("-o", "--saida", required=True)
    ap.add_argument("--voz", default="divina", help="apelido (divina/chilena) ou voice_id")
    ap.add_argument("--modelo", default="eleven_multilingual_v2")
    ap.add_argument("--estabilidade", type=float, default=0.5)
    ap.add_argument("--velocidade", type=float, default=1.0)
    ap.add_argument("--sim", action="store_true", help="não pergunta antes de gastar")
    a = ap.parse_args()
    texto = Path(a.arquivo).read_text(encoding="utf-8").strip() if a.arquivo else a.texto
    if not texto:
        raise SystemExit("Passe o texto ou --arquivo.")
    custo = len(texto) / 1000 * USD_POR_1000
    print(f"{len(texto)} caracteres ≈ US${custo:.3f} (voz {a.voz})")
    if not a.sim and input("Gerar? [s/N] ").strip().lower() != "s":
        return
    mp3, js = gerar(texto, a.saida, a.voz, a.modelo, a.estabilidade, velocidade=a.velocidade)
    print("ok:", mp3, "|", js)


if __name__ == "__main__":
    main()

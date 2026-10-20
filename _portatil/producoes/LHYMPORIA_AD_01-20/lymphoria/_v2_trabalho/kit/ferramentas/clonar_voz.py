# -*- coding: utf-8 -*-
"""Clona (Instant Voice Clone do ElevenLabs) a voz do narrador de um criativo original.
Use quando for trocar marca/oferta de um criativo próprio e a fala nova precisa da MESMA voz.

  python clonar_voz.py video_ou_audio.mp4 --nome "AD04 narrador" [--de 28 --ate 107]
  -> imprime o voice_id (use em: tts_elevenlabs.py ... --voz <voice_id>)

Pega um trecho de fala contínua (ideal 1–2 min), remove ruído/trilha no ElevenLabs e cria a voz.
A clonagem instantânea não cobra por uso no plano (só os caracteres que forem gerados depois).
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import requests

from tts_elevenlabs import chave


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("midia")
    ap.add_argument("--nome", required=True)
    ap.add_argument("--de", type=float, default=0)
    ap.add_argument("--ate", type=float, default=None)
    a = ap.parse_args()

    amostra = Path(tempfile.mkdtemp(prefix="clone_")) / "amostra.mp3"
    corte = ["-ss", str(a.de)] + (["-t", str(a.ate - a.de)] if a.ate else [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *corte, "-i", a.midia, "-vn", "-ac", "1", "-ar", "44100",
                    "-b:a", "192k", str(amostra)], check=True)
    r = requests.post("https://api.elevenlabs.io/v1/voices/add", headers={"xi-api-key": chave()},
                      data={"name": a.nome, "remove_background_noise": "true",
                            "description": "Clone do narrador do criativo original (marca própria)"},
                      files={"files": ("amostra.mp3", open(amostra, "rb"), "audio/mpeg")}, timeout=300)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:500]}")
    print("voice_id:", r.json()["voice_id"])


if __name__ == "__main__":
    main()

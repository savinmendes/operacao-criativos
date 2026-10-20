# -*- coding: utf-8 -*-
"""Dublagem automática (ElevenLabs Dubbing) de um trecho de vídeo para outro idioma, mantendo as vozes
(clonadas automaticamente por personagem) e o som de fundo. Sem marca d'água. Usa créditos do plano.

  python dublar.py video.mp4 saida_audio.mp3 --de es --para it [--ate 52.4]
Mostra progresso e tempo restante; salva o áudio dublado (mesma duração do trecho).
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
import time
from pathlib import Path

import requests

from tts_elevenlabs import chave

API = "https://api.elevenlabs.io/v1/dubbing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("saida")
    ap.add_argument("--de", default="es")
    ap.add_argument("--para", default="it")
    ap.add_argument("--ate", type=float, default=None)
    a = ap.parse_args()
    k = {"xi-api-key": chave()}
    wk = Path(tempfile.mkdtemp(prefix="dub_"))
    trecho = wk / "trecho.mp4"
    corte = ["-t", f"{a.ate:.3f}"] if a.ate else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, *corte, "-vf", "scale=360:-2", "-c:v", "libx264",
                    "-crf", "28", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", str(trecho)], check=True)
    with open(trecho, "rb") as f:
        r = requests.post(API, headers=k, files={"file": ("trecho.mp4", f, "video/mp4")},
                          data={"source_lang": a.de, "target_lang": a.para, "num_speakers": "0",
                                "watermark": "false", "name": Path(a.video).stem + f"_{a.para}"}, timeout=600)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:500]}")
    j = r.json()
    did, prev = j["dubbing_id"], float(j.get("expected_duration_sec") or 60)
    print(f"dubbing_id={did} | previsto ~{prev:.0f}s", flush=True)
    t0 = time.time()
    while True:
        time.sleep(10)
        s = requests.get(f"{API}/{did}", headers=k, timeout=60).json()
        st = s.get("status")
        dec = time.time() - t0
        print(f"[dublagem] {st} | decorrido {dec:.0f}s | falta ~{max(0, prev - dec):.0f}s", flush=True)
        if st == "dubbed":
            break
        if st in ("failed", "error"):
            raise SystemExit(f"falhou: {s}")
        if dec > 3600:
            raise SystemExit("timeout de 1 h")
    au = requests.get(f"{API}/{did}/audio/{a.para}", headers=k, timeout=600)
    au.raise_for_status()
    bruto = wk / "dub.mp4"
    bruto.write_bytes(au.content)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-vn", "-ac", "2", "-ar", "48000",
                    "-b:a", "192k", a.saida], check=True)
    print(f"ok: {a.saida} (dubbing_id={did})")


if __name__ == "__main__":
    main()

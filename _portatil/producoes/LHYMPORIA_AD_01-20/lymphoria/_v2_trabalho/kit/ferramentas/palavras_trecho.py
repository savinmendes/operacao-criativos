# -*- coding: utf-8 -*-
"""Transcreve um trecho de vídeo com tempo por palavra (faster-whisper), para achar pontos de corte.
  python palavras_trecho.py video.mp4 --de 40 [--ate 80] [--modelo small]
Imprime "tempo:palavra" (tempo absoluto no vídeo)."""
import argparse
import subprocess
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--de", type=float, default=0)
ap.add_argument("--ate", type=float, default=None)
ap.add_argument("--modelo", default="small")
a = ap.parse_args()
wav = Path(tempfile.mkdtemp()) / "t.wav"
corte = ["-ss", str(a.de)] + (["-to", str(a.ate)] if a.ate else [])
subprocess.run(["ffmpeg", "-v", "error", "-y", *corte, "-i", a.video, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel(a.modelo, device="cpu", compute_type="int8")  # CUDA do ctranslate2 não tem cuBLAS neste PC
segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True)
for s in segs:
    print(" ".join(f"{a.de + w.start:.2f}:{w.word.strip()}" for w in s.words), flush=True)

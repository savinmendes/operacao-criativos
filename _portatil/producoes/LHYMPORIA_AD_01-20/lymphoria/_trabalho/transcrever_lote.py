# -*- coding: utf-8 -*-
"""Transcrição palavra a palavra (faster-whisper small, CPU) de vários ADs -> transcricoes_palavras/AD NN.json
Mostra progresso e tempo restante."""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from faster_whisper import WhisperModel

S = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20")
OUT = S / "lymphoria" / "_trabalho" / "transcricoes_palavras"
OUT.mkdir(parents=True, exist_ok=True)
ads = sys.argv[1:]
m = WhisperModel("small", device="cpu", compute_type="int8")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


durs = {a: dur(S / f"AD {a}.mp4") for a in ads}
total, feito, t0 = sum(durs.values()), 0.0, time.time()
for a in ads:
    dst = OUT / f"AD {a}.json"
    if not dst.exists():
        wav = Path(tempfile.mkdtemp()) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(S / f"AD {a}.mp4"), "-vn", "-ac", "1", "-ar", "16000",
                        str(wav)], check=True)
        segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True)
        pal = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
        dst.write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
    feito += durs[a]
    dec = time.time() - t0
    print(f"[transcrição] AD {a} | {feito / total:.0%} | decorrido {dec / 60:.1f} min | "
          f"falta ~{dec / feito * (total - feito) / 60:.1f} min", flush=True)

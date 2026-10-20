# -*- coding: utf-8 -*-
"""Transcrição por palavra (faster-whisper small, cpu_threads=4): python transc_pal.py NN [NN...] -> adNN/palavras.json"""
import json, subprocess, sys, tempfile
from pathlib import Path
from faster_whisper import WhisperModel
B = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM")
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for n in sys.argv[1:]:
    src = Path(n) if n.endswith(".mp4") else B / "originais" / f"{n}.mp4"
    dst = (B / "producao" / "_trabalho" / f"ad{n}" / "palavras.json") if not n.endswith(".mp4") else Path(n).with_suffix(".palavras.json")
    wav = Path(tempfile.mkdtemp()) / "a.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True)
    pal = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
    dst.write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
    print("ok", n, len(pal), flush=True)

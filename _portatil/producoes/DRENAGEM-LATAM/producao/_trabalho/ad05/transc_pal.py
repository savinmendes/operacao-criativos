# -*- coding: utf-8 -*-
"""Transcrição palavra a palavra: python transc_pal.py video.mp4 saida.json"""
import json, subprocess, sys, tempfile
from pathlib import Path
from faster_whisper import WhisperModel
v, dst = sys.argv[1], sys.argv[2]
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True)
pal = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
Path(dst).write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
print("ok", len(pal))

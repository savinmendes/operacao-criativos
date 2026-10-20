# -*- coding: utf-8 -*-
"""Transcreve arquivos (es) com tempo por palavra: python transcrever.py a.mp3 b.mp4 ..."""
import sys
from faster_whisper import WhisperModel

m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="es", word_timestamps=True, vad_filter=False)
    ws = [w for s in segs for w in s.words]
    print(f"== {f}")
    print("   " + " ".join(f"{w.word.strip()}[{w.start:.2f}-{w.end:.2f}]" for w in ws))

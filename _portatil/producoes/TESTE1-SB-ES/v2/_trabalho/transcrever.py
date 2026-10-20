# -*- coding: utf-8 -*-
"""faster-whisper (cpu int8, es) com tempo por palavra. Uso: python transcrever.py video.mp4 [saida.json]"""
import json, sys
from faster_whisper import WhisperModel
arq = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(arq, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
W = []
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    for w in s.words: W.append(dict(w=w.word.strip(), ini=round(w.start, 3), fim=round(w.end, 3), p=round(w.probability, 2)))
print(" ".join(f"{w['w']}({w['ini']:.2f}-{w['fim']:.2f})" for w in W))
if out: json.dump(W, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

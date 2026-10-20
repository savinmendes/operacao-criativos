# -*- coding: utf-8 -*-
import json, subprocess, sys, re, unicodedata
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
TERMOS = ["maya", "verra", "mayaverra", "sesenta", "60 d", "hecho en", "estados unidos", "ozempic", "tiktok", "cofepris",
          "cancer", "cáncer", "precio", "link", "enlace", "dolar", "pesos", "kilos", "libras"]
for v in sys.argv[1:]:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", "rev.wav"], check=True)
    segs, _ = m.transcribe("rev.wav", language="es")
    txt = []
    for s in segs:
        txt.append(f"{s.start:7.1f} {s.text.strip()}")
    full = "\n".join(txt)
    out = v.rsplit(".", 1)[0] + "_transcricao.txt"
    open(out, "w", encoding="utf-8").write(full)
    print("==", v)
    low = full.lower()
    for t in TERMOS:
        for l in full.split("\n"):
            if t in l.lower():
                print(f"  [{t}] {l}")
    print("  últimas:", "\n".join(txt[-3:]))

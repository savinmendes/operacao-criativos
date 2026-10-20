# -*- coding: utf-8 -*-
"""Transcreve dub_it.mp3 de cada AD italiano (palavras com tempo) e lista menções de marca."""
import json, re, sys
from pathlib import Path
from faster_whisper import WhisperModel
T = Path(__file__).parent
m = WhisperModel(__import__("os").environ.get("WM","medium"), device="cpu", compute_type="int8")
for ad in sys.argv[1:]:
    p = T / ad
    out = p / "dub_it_palavras.json"
    if not out.exists():
        segs, _ = m.transcribe(str(p / "dub_it.mp3"), language="it", word_timestamps=True)
        ws = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in segs for w in s.words]
        out.write_text(json.dumps(ws, ensure_ascii=False), encoding="utf-8")
    ws = json.loads(out.read_text(encoding="utf-8"))
    print("==", ad, len(ws), "palavras")
    for i, (w, a, b) in enumerate(ws):
        if re.search(r"maya|verra|lymph|limf|linf|herbal|mayav", w, re.I):
            ctx = " ".join(x[0] for x in ws[max(0, i-6):i+6])
            print(f"  {a:7.2f}-{b:7.2f}  {w}  | {ctx}", flush=True)

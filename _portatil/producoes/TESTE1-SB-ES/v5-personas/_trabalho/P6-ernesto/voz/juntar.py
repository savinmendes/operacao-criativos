# -*- coding: utf-8 -*-
"""Junta as falas em jobs HeyGen (<= ~12 s) com 0,25 s entre frases -> J*.wav + J*.json (palavras com tempo, frase de origem)"""
import json, subprocess
import numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; SR = 48000; GAP = 0.25
JOBS = {"J1": ["E1", "E2"], "J2": ["E3", "E4"], "J3": ["P1", "P2"], "J4": ["P3", "P4"], "JR1": ["R01"], "JRC": ["RCTA"], "JR0": ["R00"]}
def load(p): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
for j, L in JOBS.items():
    out = np.zeros(0, np.float32); W = []
    for k, i in enumerate(L):
        if k: out = np.concatenate([out, np.zeros(int(GAP * SR), np.float32)])
        t0 = len(out) / SR; a = load(AQ / f"{i}.wav"); d = json.load(open(AQ / f"{i}.json", encoding="utf-8"))
        W += [dict(p, ini=round(p["ini"] + t0, 3), fim=round(p["fim"] + t0, 3), frase=i) for p in d["palavras"]]
        out = np.concatenate([out, a])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(AQ / f"{j}.wav")], input=out.tobytes(), check=True)
    json.dump(dict(dur=round(len(out) / SR, 3), frases=L, palavras=W), open(AQ / f"{j}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(j, round(len(out) / SR, 2), (AQ / f"{j}.wav").stat().st_size)

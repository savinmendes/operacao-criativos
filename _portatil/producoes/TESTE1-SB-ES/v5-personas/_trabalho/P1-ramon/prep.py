# -*- coding: utf-8 -*-
"""encurta pausas > 0,25 s (como entrevista/prep_audio.py) -> <id>.wav 48k + <id>.json (palavras). Uso: python prep.py A01B"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\voz")
from palavras import palavras
AQ = Path(__file__).resolve().parent / "audio"; SR = 48000; MAXP, LEAD, TAIL = 0.22, 0.12, 0.20
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
for i in sys.argv[1:]:
    a = load(AQ / f"{i}.mp3"); P = palavras(AQ / f"{i}.alinhamento.json")
    t0 = max(0.0, P[0]["ini"] - LEAD); t1 = min(len(a) / SR, P[-1]["fim"] + TAIL); cortes = []
    for x, y in zip(P, P[1:]):
        g = y["ini"] - x["fim"]
        if g > MAXP: c0 = x["fim"] + MAXP / 2; cortes.append((c0, c0 + g - MAXP))
    keep, t = [], t0
    for c0, c1 in cortes: keep.append((t, c0)); t = c1
    keep.append((t, t1)); xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for x, y in keep:
        p = a[int(x * SR):int(y * SR)].copy()
        if len(out) and len(p) > xf: p[:xf] *= np.linspace(0, 1, xf); out[-xf:] *= np.linspace(1, 0, xf)
        out = np.concatenate([out, p])
    def m(tt): return round(tt - t0 - sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes), 3)
    W = [dict(w=p["w"], ini=m(p["ini"]), fim=m(p["fim"])) for p in P]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(AQ / f"{i}.wav")], input=out.tobytes(), check=True)
    (AQ / f"{i}.json").write_text(json.dumps(dict(dur=round(len(out) / SR, 3), palavras=W, cortes=cortes), ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, f"{len(a)/SR:.2f} -> {len(out)/SR:.2f}", "cortes", cortes)

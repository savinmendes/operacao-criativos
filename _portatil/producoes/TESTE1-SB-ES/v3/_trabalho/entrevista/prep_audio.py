# -*- coding: utf-8 -*-
"""Encurta pausas entre palavras > MAXP para MAXP (corte no meio do silencio, micro-fade), mantem LEAD antes da 1a palavra e TAIL depois da ultima.
Saida: audio/<id>.wav (48k mono) + audio/<id>.json (palavras remapeadas, pausas). Uso: python prep_audio.py"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\voz")
from palavras import palavras
AQ = Path(__file__).resolve().parent / "audio"; SR = 48000; MAXP, LEAD, TAIL = 0.25, 0.12, 0.20
def load(p):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
res = {}
for f in json.loads((AQ.parent / "falas.json").read_text(encoding="utf-8")):
    i = f["id"]; a = load(AQ / f"{i}.mp3"); P = palavras(AQ / f"{i}.alinhamento.json")
    t0 = max(0.0, P[0]["ini"] - LEAD); t1 = min(len(a) / SR, P[-1]["fim"] + TAIL)
    cortes = []
    for x, y in zip(P, P[1:]):
        g = y["ini"] - x["fim"]
        if g > MAXP:
            rem = g - MAXP; c0 = x["fim"] + MAXP / 2; cortes.append((c0, c0 + rem))
    keep, t = [], t0
    for c0, c1 in cortes: keep.append((t, c0)); t = c1
    keep.append((t, t1))
    xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for x, y in keep:
        p = a[int(x * SR):int(y * SR)].copy()
        if len(out) and len(p) > xf:
            p[:xf] *= np.linspace(0, 1, xf); out[-xf:] *= np.linspace(1, 0, xf); out = np.concatenate([out, p])
        else: out = np.concatenate([out, p])
    def m(tt):
        d = t0 + sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes); return round(tt - d, 3)
    W = [dict(w=p["w"], ini=m(p["ini"]), fim=m(p["fim"])) for p in P]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(AQ / f"{i}.wav")],
                   input=out.astype(np.float32).tobytes(), check=True)
    gaps = [(W[k]["fim"], W[k + 1]["ini"]) for k in range(len(W) - 1) if W[k + 1]["ini"] - W[k]["fim"] >= 0.12]
    res[i] = dict(arquivo=f"audio/{i}.wav", texto=f["t"], dur=round(len(out) / SR, 3), corte_fonte=[round(t0, 3), round(t1, 3)],
                  pausas_removidas=[[round(c0, 3), round(c1, 3)] for c0, c1 in cortes], palavras=W, pausas_restantes=gaps)
    print(i, f"{len(a)/SR:.2f} -> {len(out)/SR:.2f}", "cortes", len(cortes), "gaps", gaps)
(AQ / "partes.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

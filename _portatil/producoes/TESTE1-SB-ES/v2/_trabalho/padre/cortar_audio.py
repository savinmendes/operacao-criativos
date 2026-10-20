# -*- coding: utf-8 -*-
"""Recorta as falas do padre: takes de avatar (pausas internas <= 0,25 s) e narrações (pausas naturais).
Saída: audio/<id>.wav (48 kHz estéreo) + audio/<id>.json {texto, dur, palavras, pausas}. Uso: python cortar_audio.py"""
import json, subprocess, sys, numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; V = AQ.parent.parent.parent / "_trabalho" / "voz"; A = AQ / "audio"; SR = 48000
sys.path.insert(0, str(V)); from palavras import palavras
def load(p):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
def fonte(n):
    if n == "P6": return load(A / "P6_tts.mp3"), palavras(A / "P6_tts.alinhamento.json")
    return load(V / "c" / f"{n}.wav"), json.loads((V / "c" / f"{n}.json").read_text(encoding="utf-8"))["palavras"]
ITENS = [  # id, fonte, palavra i0, i1 (inclusive), avatar?
    ("P1", "L08", 0, 19, True), ("P2", "L08", 20, 31, True), ("narr_L08_no-quieren", "L08", 32, 44, False), ("P3", "L08", 45, 46, True),
    ("P4", "L10", 0, 19, True), ("P5", "L10", 20, 35, True), ("narr_L10_monjes-congreso", "L10", 36, None, False),
    ("narr_L11_imagina", "L11", 0, None, False), ("P6", "P6", 0, None, True)]
MAXP, LEAD, TAIL, F = 0.25, 0.10, 0.18, int(0.006 * SR)
out = {}
for iid, src, i0, i1, av in ITENS:
    a, P = fonte(src); i1 = len(P) - 1 if i1 is None else i1; W = P[i0:i1 + 1]
    t0 = max(W[0]["ini"] - LEAD, (P[i0 - 1]["fim"] + W[0]["ini"]) / 2 if i0 > 0 else 0)
    t1 = min(W[-1]["fim"] + TAIL, (W[-1]["fim"] + P[i1 + 1]["ini"]) / 2 if i1 + 1 < len(P) else len(a) / SR)
    cortes = []
    if av:
        for x, y in zip(W, W[1:]):
            g = y["ini"] - x["fim"]
            if g > MAXP: rem = g - MAXP; c0 = x["fim"] + MAXP / 2; cortes.append((c0, c0 + rem))
    partes, t = [], t0
    for c0, c1 in cortes: partes.append(a[int(t * SR):int(c0 * SR)].copy()); t = c1
    partes.append(a[int(t * SR):int(t1 * SR)].copy())
    for k, p in enumerate(partes):
        if k > 0: p[:F] *= np.linspace(0, 1, F)[:, None]
        if k < len(partes) - 1: p[-F:] *= np.linspace(1, 0, F)[:, None]
    y = np.concatenate(partes); n = int(0.01 * SR); y[:n] *= np.linspace(0, 1, n)[:, None]; y[-n:] *= np.linspace(1, 0, n)[:, None]
    def m(tt): return round(tt - t0 - sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes), 3)
    WW = [dict(w=w["w"], ini=m(w["ini"]), fim=m(w["fim"])) for w in W]
    dur = round(len(y) / SR, 3)
    pausas = [[0.0, WW[0]["ini"]]] + [[x["fim"], z["ini"]] for x, z in zip(WW, WW[1:]) if z["ini"] - x["fim"] >= 0.15] + [[WW[-1]["fim"], dur]]
    raw = A / "_t.f32"; raw.write_bytes(y.astype(np.float32).tobytes())
    dst = (AQ / f"{iid}.wav") if iid.startswith("narr") else (A / f"{iid}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-c:a", "pcm_s16le", str(dst)]); raw.unlink()
    txt = " ".join(w["w"] for w in WW)
    out[iid] = dict(arquivo=dst.name, texto=txt, dur=dur, palavras=WW, pausas=[[round(p, 3), round(q, 3)] for p, q in pausas], avatar=av, fonte=src)
    print(f"{iid:28s} {dur:6.2f}s  cortes={len(cortes)}  {txt}")
json.dump(out, open(A / "itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

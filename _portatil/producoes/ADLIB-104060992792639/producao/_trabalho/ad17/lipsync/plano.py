# -*- coding: utf-8 -*-
"""Plano de recorte que SEGUE o rosto de quem fala (mulher), por quadro, para o lipsync do HeyGen.
Gera lipsync/caixas_<seg>.npy: por quadro [x0, y0, w, h, mx, my, fw, fh] (recorte 9:16 + boca + tamanho do rosto)."""
import json, sys, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text())
R = json.loads((AD / "_tmp/rostos.json").read_text())
W, H = 720, 1280
def escolher(fs):
    fs = [f for f in fs if f[2] - f[0] >= 70]
    if not fs: return None, []
    big = [f for f in fs if f[2] - f[0] > 200]
    if big: w = max(big, key=lambda f: f[2] - f[0])
    else:
        cand = [f for f in fs if 340 <= (f[0] + f[2]) / 2 <= 620] or fs
        w = min(cand, key=lambda f: abs((f[0] + f[2]) / 2 - 470))
    return w, [f for f in fs if f is not w]
amostras = {}
for shot, L in R.items():
    for i, fs in L:
        w, outros = escolher(fs)
        if w: amostras[i] = (w, outros)
ks = np.array(sorted(amostras))
def caixa(i):
    # interpola o rosto da mulher entre amostras do mesmo plano
    j = np.searchsorted(ks, i)
    a = ks[max(0, j - 1)] if j > 0 else ks[0]; b = ks[min(j, len(ks) - 1)]
    if CFG["seg_de"](i) if False else False: pass
    return a, b
def calc(seg):
    a0, b0 = seg["a"], seg["b"]
    loc = [k for k in ks if a0 <= k < b0]
    out = []
    for i in range(a0, b0):
        lo = [k for k in loc if k <= i]; hi = [k for k in loc if k >= i]
        ka = lo[-1] if lo else hi[0]; kb = hi[0] if hi else lo[-1]
        t = 0 if kb == ka else (i - ka) / (kb - ka)
        fa, fb = np.array(amostras[ka][0], float), np.array(amostras[kb][0], float)
        f = fa * (1 - t) + fb * t
        outros = amostras[ka][1] + amostras[kb][1]
        out.append((f, outros))
    F = np.array([o[0] for o in out])
    k = 9; pad = np.pad(F, ((k // 2, k // 2), (0, 0)), mode="edge")
    F = np.array([pad[i:i + k].mean(0) for i in range(len(F))])
    cx_ = []
    for (f0, outros), f in zip(out, F):
        fx0, fy0, fx1, fy1, mx, my = f; fw, fh = fx1 - fx0, fy1 - fy0
        cw = min(W, max(seg.get("min_w", 288), seg.get("fator", 2.4) * fw)); ch = cw * 16 / 9
        if ch > H: ch = H; cw = ch * 9 / 16
        cx = (fx0 + fx1) / 2; cy = (fy0 + fy1) / 2 + 0.12 * ch
        x0 = cx - cw / 2
        for o in outros:   # empurra o recorte para fora de outro rosto a esquerda
            if (o[0] + o[2]) / 2 < cx and o[2] > x0 and seg.get("evitar", True): x0 = min(o[2] + 4, fx0 - seg.get("margem", 0.25) * fw)
        x0 = float(np.clip(x0, 0, W - cw)); y0 = float(np.clip(cy - ch / 2, 0, H - ch))
        cx_.append([x0, y0, cw, ch, mx, my, fw, fh])
    C = np.array(cx_)
    pad = np.pad(C[:, :4], ((k // 2, k // 2), (0, 0)), mode="edge")
    C[:, :4] = np.array([pad[i:i + k].mean(0) for i in range(len(C))])
    return C
for s in CFG["segs"]:
    if s.get("cheio"):
        C = calc(s); C[:, :4] = [0, 0, W, H]
    else: C = calc(s)
    np.save(AQ / f"caixas_{s['nome']}.npy", C)
    print(s["nome"], s["a"], s["b"], "rec w", C[:, 2].min().round(), "-", C[:, 2].max().round(), "x0", C[:, 0].min().round(), "-", C[:, 0].max().round(), "y0", C[:, 1].min().round(), "-", C[:, 1].max().round())

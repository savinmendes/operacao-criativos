# -*- coding: utf-8 -*-
"""Degrau robusto ao formato da boca (= _ad1718/degrau_mediana.py, para os ADs 10/15/16): MEDIANA de (base_lipsync -
original) dentro da elipse colada (0,8x) contra o anel de pele fora dela (1,3x-1,9x), por trecho, luma.
A mediana ignora o +/- do labio que mudou de lugar; um degrau de cor desloca a mediana inteira.
Na abertura reenquadrada (10/16) o original e recortado igual. Uso: python degrau_mediana_geo.py NN [base_lipsync.mp4]"""
import sys, json, numpy as np, cv2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cor_trecho import quadros
NN = sys.argv[1]; T = Path(__file__).resolve().parents[1]; AD = T / f"ad{NN}"; P = T.parents[1]
ARQ = AD / (sys.argv[2] if len(sys.argv) > 2 else "base_lipsync.mp4")
REC = {"10": (400, 230, 320, 569, 232), "16": (200, 180, 360, 640, 291)}.get(NN)
el = {}   # quadro -> (nome, cx, cy, ax, ay)
if NN == "10":
    C = json.loads((AD / "lipsync" / "segs.json").read_text())["segs"]
    for s in C:
        bx = json.loads((AD / "lipsync" / "boxes" / f"{s['nome']}.json").read_text())
        for k in range(0, bx["n"], 4):
            x0, y0, x1, y1 = bx["boxes"][k]["face"]; fw, fh = x1 - x0, y1 - y0
            el[s["q"][0] + k] = (s["nome"], (x0 + x1) / 2, y0 + 0.70 * fh, 0.38 * fw, 0.32 * fh)
else:
    segs = json.loads((AD / "lipsync" / ("segs_i1r.json" if NN == "16" else "segs.json")).read_text())["segs"]
    tro = {"i1r": "i1s", "j1": "j1b", "k1": "k1b"} if NN == "16" else {}
    for s in segs:
        a, b = s["q0"], s["q1"]
        for k in range(0, b - a + 1, 4):
            if s["nome"] in tro:
                Tr = json.loads((AD / "lipsync_b" / "trilhas" / f"{tro[s['nome']]}.json").read_text()); r = Tr["rosto"][k]
                fw, fh = r[2] - r[0], r[3] - r[1]; el[a + k] = (s["nome"], (r[0] + r[2]) / 2, r[1] + 0.68 * fh, 0.42 * fw + 6, 0.36 * fh + 8)
            else:
                c = s["cola"]
                if c is None: continue
                if isinstance(c[0], (list, tuple)):
                    K = np.array(c, float); c = [np.interp(k, K[:, 0], K[:, j]) for j in range(1, 5)]
                el[a + k] = (s["nome"], *c)
mx = max(el) + 1; F = quadros(ARQ, 0, mx); O = quadros(P / "UNICOS_HD" / f"{NN}.mp4", 0, mx); res = {}
for i in range(mx):
    f, o = next(F), next(O)
    if i not in el: continue
    if REC and i <= REC[4]:
        x, y, w, h, _ = REC; o = cv2.resize(o[y:y + h, x:x + w], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
    nm, cx, cy, ax, ay = el[i]; ctr = (int(cx), int(cy))
    def E(s): m = np.zeros((1280, 720), np.uint8); cv2.ellipse(m, ctr, (int(ax * s), int(ay * s)), 0, 0, 360, 1, -1); return m > 0
    d = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float) - cv2.cvtColor(o, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    res.setdefault(nm, []).append((np.median(d[E(0.8)]), np.median(d[E(1.9) & ~E(1.3)])))
tot = []
print(f"AD {NN} ({ARQ.name}): mediana base-original | elipse colada | anel fora | degrau")
for nm, v in res.items():
    v = np.median(np.array(v), 0); tot.append(v); print(f"  {nm:5} {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")

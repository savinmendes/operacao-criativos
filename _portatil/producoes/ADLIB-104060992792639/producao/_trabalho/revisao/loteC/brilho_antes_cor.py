# -*- coding: utf-8 -*-
"""Revisor (lote C): brilho da area colada (boca/queixo) x resto do rosto x fundo, FINAL - ORIGINAL (luma Y, 0-255).
Por trecho: dY_boca (labio sup + queixo, dentro da elipse colada), dY_face (bochechas/olhos, fora da elipse),
dY_fundo (quadro inteiro fora do rosto). Uso: python brilho.py NN pasta_escolha [passo=3]"""
import sys, json
from pathlib import Path
import numpy as np, cv2
NN, pasta = sys.argv[1], Path(sys.argv[2]); passo = int(sys.argv[3]) if len(sys.argv) > 3 else 3
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao" / "_trabalho" / f"ad{NN}" / "_antes_cor").glob(f"AD {NN} - *-ES-LATAM.mp4")); ORI = P / "UNICOS_HD" / f"{NN}.mp4"
esc = json.loads((pasta / f"escolha_{NN}.json").read_text())
mapa = (lambda t: t if t * 24 < 1286 else t + 70 / 24) if NN == "05" else (lambda t: t)
pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[q] = (k, cx, cy, L)
cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI)); fpo = co.get(cv2.CAP_PROP_FPS)
def Y(img): return cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
def box(y, cx, cy, w, h):
    x0, y0 = int(max(0, cx - w / 2)), int(max(0, cy - h / 2)); return y[y0:int(y0 + h), x0:int(x0 + w)]
res = {}; oi = -1; o = None; q = 0
while True:
    ok, f = cf.read()
    if not ok: break
    want = int(round(mapa(q / 30) * fpo))
    while oi < want:
        ok2, o2 = co.read(); oi += 1
        if ok2: o = o2
    if q in pos and q % passo == 0 and o is not None:
        k, cx, cy, L = pos[q]; yf, yo = Y(f), Y(o)
        d = lambda *a: float(np.mean(box(yf, *a)) - np.mean(box(yo, *a)))
        boca = (d(cx, cy - 0.17 * L, 0.30 * L, 0.08 * L) + d(cx, cy + 0.30 * L, 0.30 * L, 0.12 * L)) / 2
        face = (d(cx - 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L) + d(cx + 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L)) / 2
        m = np.ones_like(yf, bool); m[int(max(0, cy - 1.6 * L)):int(cy + 1.0 * L), int(max(0, cx - 0.9 * L)):int(cx + 0.9 * L)] = False
        fundo = float(yf[m].mean() - yo[m].mean())
        res.setdefault(k, []).append((boca, face, fundo))
    q += 1
print(f"AD {NN}: dY = final - original (luma 0-255); 'boca-face' = degrau da elipse colada contra o rosto")
tot = []
for k in esc:
    if k not in res: continue
    r = np.array(res[k]); tot += res[k]
    print(f"{k:9} boca {np.median(r[:,0]):+5.1f}  face {np.median(r[:,1]):+5.1f}  fundo {np.median(r[:,2]):+5.1f}  | boca-face {np.median(r[:,0]-r[:,1]):+5.1f}  (n={len(r)})")
r = np.array(tot); print(f"TODOS     boca {np.median(r[:,0]):+5.1f}  face {np.median(r[:,1]):+5.1f}  fundo {np.median(r[:,2]):+5.1f}  | boca-face {np.median(r[:,0]-r[:,1]):+5.1f}")

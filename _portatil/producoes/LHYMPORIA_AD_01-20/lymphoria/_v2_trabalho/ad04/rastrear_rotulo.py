# -*- coding: utf-8 -*-
"""Rastreia a faixa do rótulo do concorrente (template do quadro de referência) e
mede posição/escala por quadro. Saída: rastreio.json  {frame: [x, y, escala, score]} em px do vídeo 360p."""
import json
import sys

import cv2
import numpy as np

src, ref_t, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
X0, Y0, X1, Y1 = 175, 468, 268, 487          # faixa no quadro de referência (360p)
T_INI, T_FIM = 4.0, 32.0                      # janela onde o frasco aparece

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(ref_t * fps))
ok, ref = cap.read()
tpl = cv2.cvtColor(ref[Y0:Y1, X0:X1], cv2.COLOR_BGR2GRAY)

res = {}
cap.set(cv2.CAP_PROP_POS_FRAMES, int(T_INI * fps))
f = int(T_INI * fps)
while f < int(T_FIM * fps):
    ok, im = cap.read()
    if not ok:
        break
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    best = (0, None, None)
    for s in np.arange(0.7, 1.45, 0.05):
        t = cv2.resize(tpl, None, fx=s, fy=s)
        if t.shape[0] >= g.shape[0] or t.shape[1] >= g.shape[1]:
            continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]:
            best = (mx, loc, s)
    if best[1] is not None:
        res[f] = [best[1][0], best[1][1], round(float(best[2]), 3), round(float(best[0]), 3)]
    f += 1

json.dump(res, open(out, "w"), indent=0)
bons = [k for k, v in res.items() if v[3] >= 0.6]
print(f"fps={fps} quadros={len(res)} com_match>=0.6: {len(bons)}")
# trechos contínuos
tre, ini, ant = [], None, None
for k in sorted(bons):
    if ini is None:
        ini = ant = k
    elif k - ant > 3:
        tre.append((ini, ant)); ini = k
    ant = k
if ini is not None:
    tre.append((ini, ant))
for a, b in tre:
    print(f"  {a/fps:6.2f}s – {b/fps:6.2f}s")

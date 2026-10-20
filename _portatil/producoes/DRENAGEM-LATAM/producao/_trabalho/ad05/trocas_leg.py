# -*- coding: utf-8 -*-
"""Acha os instantes em que a legenda queimada muda numa faixa e salva um recorte de cada bloco.
python trocas_leg.py video t0 t1 y0 y1 pasta"""
import sys, cv2, numpy as np, os
v, t0, t1, y0, y1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
os.makedirs(out, exist_ok=True)
c = cv2.VideoCapture(v); fps = c.get(cv2.CAP_PROP_FPS)
c.set(cv2.CAP_PROP_POS_FRAMES, int(t0 * fps)); f = int(t0 * fps); prev = None; blocos = []
while f <= t1 * fps:
    ok, fr = c.read()
    if not ok: break
    roi = fr[y0:y1]; m = ((roi.min(axis=2) > 215)).astype(np.uint8)
    if prev is None or (m ^ prev).sum() > 0.25 * max(1, max(m.sum(), prev.sum())):
        blocos.append((f / fps, fr[y0:y1].copy()))
    prev = m; f += 1
for i, (t, r) in enumerate(blocos):
    cv2.imwrite(f"{out}/{i:02d}_{t:.2f}.png", r); print(f"{t:.3f}")

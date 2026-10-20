# -*- coding: utf-8 -*-
"""Tira de recortes (faixa y0-y1) a cada passo, com o tempo escrito. python tira.py video t0 t1 passo y0 y1 out.jpg"""
import sys, cv2, numpy as np
v, t0, t1, p, y0, y1, out = sys.argv[1], *map(float, sys.argv[2:5]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
c = cv2.VideoCapture(v); rows = []; t = t0
while t <= t1 + 1e-6:
    c.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = c.read()
    if not ok: break
    r = fr[y0:y1].copy(); cv2.putText(r, f"{t:.2f}", (5, 22), 0, 0.7, (0, 255, 255), 2); rows.append(r); t += p
cols = 4; h, w = rows[0].shape[:2]
while len(rows) % cols: rows.append(np.zeros_like(rows[0]))
cv2.imwrite(out, np.vstack([np.hstack(rows[i:i + cols]) for i in range(0, len(rows), cols)]))

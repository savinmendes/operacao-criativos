# -*- coding: utf-8 -*-
"""Folha de quadros. Uso: python folha.py video t0 t1 passo_s colunas largura saida.jpg [x0,y0,x1,y1 (recorte)]"""
import sys, cv2, numpy as np
v, t0, t1, st, cols, w, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
crop = [int(x) for x in sys.argv[8].split(",")] if len(sys.argv) > 8 else None
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS)
ims = []; t = t0
while t <= t1 + 1e-6:
    q = int(round(t * fps)); cap.set(cv2.CAP_PROP_POS_FRAMES, q); ok, f = cap.read()
    if not ok: break
    if crop: f = f[crop[1]:crop[3], crop[0]:crop[2]]
    h = int(f.shape[0] * w / f.shape[1]); f = cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA)
    cv2.putText(f, f"{t:.2f} q{q}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 3)
    cv2.putText(f, f"{t:.2f} q{q}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
    ims.append(f); t += st
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out, len(ims))

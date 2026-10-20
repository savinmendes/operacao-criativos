# -*- coding: utf-8 -*-
"""Uso: python folha.py video.mp4 t0 t1 x,y,w,h saida.jpg [passo_q]  -> folha com zoom no rosto, quadro a quadro"""
import sys, cv2, numpy as np
v, t0, t1, ro, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]; st = int(sys.argv[6]) if len(sys.argv) > 6 else 2
x, y, w, h = map(int, ro.split(",")); cap = cv2.VideoCapture(v); fps = cap.get(5); cs = []
for q in range(int(round(t0 * fps)), int(round(t1 * fps)), st):
    cap.set(1, q); ok, f = cap.read()
    if not ok: break
    c = cv2.resize(f[y:y + h, x:x + w], (200, int(200 * h / w))); cv2.putText(c, f"{q/fps:.2f}", (4, 18), 0, 0.5, (0, 255, 255), 1); cs.append(c)
rows = [np.hstack(cs[i:i + 8] + [np.zeros_like(cs[0])] * (8 - len(cs[i:i + 8]))) for i in range(0, len(cs), 8)]
cv2.imwrite(out, np.vstack(rows)); print(out, len(cs))

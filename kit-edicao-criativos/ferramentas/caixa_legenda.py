# -*- coding: utf-8 -*-
"""Acha a caixa (x0,y0,x1,y1) da legenda queimada num instante: maior grupo de letras brancas
na faixa inferior/central da tela. Imprime a caixa com margem, pronta para trocar_texto_tela.py.

  python caixa_legenda.py video.mp4 --t 2.9 [--faixa 0.45,0.92] [--debug caixa.jpg]
"""
import argparse

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--t", type=float, required=True)
ap.add_argument("--faixa", default="0.45,0.92")
ap.add_argument("--debug", default=None)
a = ap.parse_args()
c = cv2.VideoCapture(a.video)
c.set(cv2.CAP_PROP_POS_MSEC, a.t * 1000)
ok, im = c.read()
H, W = im.shape[:2]
f0, f1 = [float(x) for x in a.faixa.split(",")]
y0, y1 = int(H * f0), int(H * f1)
reg = im[y0:y1]
branco = (reg.min(2) > 225).astype(np.uint8)
escuro = (reg.max(2) < 60).astype(np.uint8)
# letra de legenda = branco com contorno escuro por perto
viz = cv2.dilate(escuro, np.ones((5, 5), np.uint8))
letras = branco & viz
letras = cv2.morphologyEx(letras, cv2.MORPH_CLOSE, np.ones((9, 25), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(letras, 8)
cand = [(st[k, 4], k) for k in range(1, n) if st[k, 3] > H * 0.012 and st[k, 2] > W * 0.06]
if not cand:
    raise SystemExit("nenhuma legenda encontrada")
_, k = max(cand)
x, y, w, h, _ = st[k]
# junta linhas vizinhas (legenda de 2 linhas)
for kk in range(1, n):
    xx, yy, ww, hh, aa = st[kk]
    if kk != k and hh > H * 0.012 and abs((yy + hh / 2) - (y + h / 2)) < h * 2.2 and xx < x + w and xx + ww > x:
        nx0, ny0 = min(x, xx), min(y, yy)
        w, h, x, y = max(x + w, xx + ww) - nx0, max(y + h, yy + hh) - ny0, nx0, ny0
m = int(h * 0.15) + 4
caixa = (max(0, x - m), max(0, y0 + y - m), min(W, x + w + m), min(H, y0 + y + h + m))
print(",".join(map(str, caixa)))
if a.debug:
    cv2.rectangle(im, caixa[:2], caixa[2:], (0, 0, 255), 3)
    cv2.imwrite(a.debug, cv2.resize(im, None, fx=0.5, fy=0.5))

# -*- coding: utf-8 -*-
"""Folha 1 em 1 quadro em volta de tempos: python folha_cortes.py video.mp4 saida.jpg t1 t2 ... [--raio 4] [--box x,y,w,h]"""
import sys, cv2, numpy as np
a = sys.argv[1:]; raio = 4; box = None
if "--raio" in a: i = a.index("--raio"); raio = int(a[i+1]); del a[i:i+2]
if "--box" in a: i = a.index("--box"); box = list(map(int, a[i+1].split(","))); del a[i:i+2]
v, saida, ts = a[0], a[1], [float(t) for t in a[2:]]
cap = cv2.VideoCapture(v); rows = []
for t in ts:
    q = int(round(t * 30)); tl = []
    for k in range(q - raio, q + raio):
        cap.set(1, max(0, k)); ok, f = cap.read()
        if not ok: f = np.zeros((1280, 720, 3), np.uint8)
        if box: x, y, w, h = box; f = f[y:y+h, x:x+w]
        f = cv2.resize(f, (144, int(144 * f.shape[0] / f.shape[1])))
        cv2.putText(f, f"{k} {k/30:.2f}", (2, 12), 0, 0.38, (0, 255, 255), 1); tl.append(f)
    rows.append(np.hstack(tl))
cv2.imwrite(saida, np.vstack(rows)); print(saida)

# -*- coding: utf-8 -*-
"""Folha com quadros em tempos escolhidos (rótulo com o tempo).
  python quadros_A.py video.mp4 saida.jpg largura colunas t1 t2 ...   (ou "passo:0.5" para todos)
"""
import sys

import cv2
import numpy as np

v, out, lw, cols = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
cap = cv2.VideoCapture(v)
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if sys.argv[5].startswith("passo:"):
    p = float(sys.argv[5].split(":")[1])
    ts = list(np.arange(0, n / fps, p))
else:
    ts = [float(x) for x in sys.argv[5:]]
ims = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, im = cap.read()
    if not ok:
        continue
    im = cv2.resize(im, (lw, int(lw * im.shape[0] / im.shape[1])))
    cv2.rectangle(im, (0, 0), (70, 22), (0, 0, 0), -1)
    cv2.putText(im, f"{t:.2f}", (3, 17), 0, 0.55, (0, 255, 255), 1)
    ims.append(im)
while len(ims) % cols:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[k:k + cols]) for k in range(0, len(ims), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85])

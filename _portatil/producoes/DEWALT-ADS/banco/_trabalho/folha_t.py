# -*- coding: utf-8 -*-
"""Folha com quadros a cada PASSO s e o tempo escrito. Uso: python folha_t.py video.mp4 saida_prefixo [passo] [ini] [fim] [cols]"""
import sys, cv2, numpy as np
v = sys.argv[1]; out = sys.argv[2]; passo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
ini = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fim = float(sys.argv[5]) if len(sys.argv) > 5 else n / fps
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 6
TW, TH = 200, 356
ts = list(np.arange(ini, fim, passo)); tiles = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps))); ok, f = cap.read()
    if not ok: continue
    f = cv2.resize(f, (TW, TH), interpolation=cv2.INTER_AREA)
    cv2.rectangle(f, (0, 0), (70, 22), (0, 0, 0), -1); cv2.putText(f, f"{t:.1f}", (3, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)
    tiles.append(f)
per = cols * 6
for k in range(0, len(tiles), per):
    grp = tiles[k:k + per]; rows = (len(grp) + cols - 1) // cols
    W = np.zeros((rows * TH, cols * TW, 3), np.uint8)
    for i, f in enumerate(grp): W[(i // cols) * TH:(i // cols + 1) * TH, (i % cols) * TW:(i % cols + 1) * TW] = f
    cv2.imwrite(f"{out}_{k // per}.jpg", W, [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(tiles), "quadros")

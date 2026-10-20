# -*- coding: utf-8 -*-
"""LaMa num print: tira barra do topo (live), rodapé de comentários e legenda queimada. Uso: _vg python lama_print.py in.png out.png"""
import sys, cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
f = cv2.imread(sys.argv[1]); H, W = f.shape[:2]; m = np.zeros((H, W), np.uint8)
m[0:100] = 1; m[1160:] = 1
roi = f[860:1010]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
txt = (((hsv[..., 0] >= 15) & (hsv[..., 0] <= 42) & (hsv[..., 1] >= 80) & (hsv[..., 2] >= 140)) | ((hsv[..., 1] < 40) & (hsv[..., 2] > 225))).astype(np.uint8)
txt &= cv2.dilate((hsv[..., 2] < 90).astype(np.uint8), np.ones((7, 7), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(txt)
for k in range(1, n):
    if st[k, cv2.CC_STAT_AREA] < 20: txt[lab == k] = 0
d = cv2.dilate(txt, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
m[860:1010] |= cv2.dilate(d, np.ones((7, 7), np.uint8))
cv2.imwrite(sys.argv[2].replace(".png", "_mask.png"), m * 255)
out = SimpleLama()(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
out.crop((0, 0, W, H)).save(sys.argv[2]); print("ok")

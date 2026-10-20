# -*- coding: utf-8 -*-
"""Folha de quadros (região x0,y0,x1,y1) nos intervalos dados, com o tempo. Uso: python qa_pausas.py take.mp4 saida.jpg "a-b,c-d" [x0,y0,x1,y1]"""
import sys, cv2, numpy as np
v, out, ivs = sys.argv[1], sys.argv[2], sys.argv[3]
x0, y0, x1, y1 = map(int, (sys.argv[4] if len(sys.argv) > 4 else "300,0,720,450").split(","))
I = [tuple(map(float, x.split("-"))) for x in ivs.split(",")]
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS); n = 0; tiles = []
while True:
    ok, f = cap.read()
    if not ok: break
    t = n / fps; n += 1
    if any(a <= t <= b for a, b in I):
        c = f[y0:y1, x0:x1]; c = cv2.resize(c, (200, int(200 * c.shape[0] / c.shape[1])))
        cv2.putText(c, f"{t:.2f}", (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2); tiles.append(c)
W = 10; h, w = tiles[0].shape[:2]; rows = (len(tiles) + W - 1) // W
img = np.zeros((rows * h, W * w, 3), np.uint8)
for i, c in enumerate(tiles): img[i // W * h:(i // W + 1) * h, i % W * w:(i % W + 1) * w] = c
cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, 85]); print(len(tiles), "quadros")

# -*- coding: utf-8 -*-
"""Desfoca regiões da tela num intervalo (ex.: marca de outra empresa numa tela de celular), com borda suave.
  python desfocar_regioes.py entrada.mp4 saida.mp4 --de 346.67 --ate 349.73 --caixas "230,110,560,215;150,660,370,705"
Áudio copiado."""
import argparse
import subprocess

import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("entrada")
ap.add_argument("saida")
ap.add_argument("--de", type=float, required=True)
ap.add_argument("--ate", type=float, required=True)
ap.add_argument("--caixas", required=True)
ap.add_argument("--forca", type=int, default=45)
a = ap.parse_args()
caixas = [tuple(map(int, c.split(","))) for c in a.caixas.split(";")]
cap = cv2.VideoCapture(a.entrada)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
mask = np.zeros((H, W), np.float32)
for x0, y0, x1, y1 in caixas:
    mask[y0:y1, x0:x1] = 1
mask = cv2.GaussianBlur(mask, (31, 31), 0)[..., None]
i0, i1 = int(round(a.de * fps)), int(round(a.ate * fps))
k = a.forca | 1
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", a.entrada, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15",
                       "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", a.saida], stdin=subprocess.PIPE)
i = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    if i0 <= i <= i1:
        b = cv2.GaussianBlur(im, (k, k), 0)
        im = (b * mask + im * (1 - mask)).astype(np.uint8)
    ff.stdin.write(im.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print(f"ok: {a.saida} | {i1 - i0 + 1} quadros desfocados")

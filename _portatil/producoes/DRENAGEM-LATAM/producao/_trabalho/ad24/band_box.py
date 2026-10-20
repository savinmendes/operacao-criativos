# -*- coding: utf-8 -*-
"""Troca o texto do rótulo dentro de uma caixa dada à mão (com chaves por quadro), para planos quase parados.
Preenche a caixa com a cor de fundo da faixa coluna a coluna (degradê preservado) e escreve o texto novo.
  python band_box.py in.mp4 out.mp4 --caixa "q:x0,y0,x1,y1;q:..." [--texto LYMPHORIA] [--alt 0.52]"""
import argparse, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("ent"); ap.add_argument("sai"); ap.add_argument("--caixa", required=True)
ap.add_argument("--texto", default="LYMPHORIA"); ap.add_argument("--alt", type=float, default=0.52)
a = ap.parse_args()
FONT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"
K = sorted((int(q), list(map(float, r.split(",")))) for q, r in (c.split(":") for c in a.caixa.split(";")))


def em(n):
    if n <= K[0][0]: return K[0][1]
    for (q0, r0), (q1, r1) in zip(K, K[1:]):
        if n <= q1:
            t = (n - q0) / (q1 - q0); return [u + (v - u) * t for u, v in zip(r0, r1)]
    return K[-1][1]


cap = cv2.VideoCapture(a.ent); W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                      "-i", "-", "-c:v", "libx264", "-crf", "13", "-pix_fmt", "yuv420p", "-r", "30", a.sai], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    x0, y0, x1, y1 = em(n)
    X0, Y0, X1, Y1 = int(x0), int(y0), int(np.ceil(x1)), int(np.ceil(y1))
    band = f[Y0:Y1, X0:X1].astype(np.float32)
    lum = band.mean(axis=2)
    cor = np.array([band[:, j][lum[:, j] <= np.percentile(lum[:, j], 40)].mean(axis=0) for j in range(X1 - X0)], np.float32)
    cor = cv2.blur(cor.reshape(1, -1, 3), (9, 1)).reshape(-1, 3)
    vert = np.array([np.percentile(lum[y], 35) for y in range(Y1 - Y0)], np.float32)
    vert = cv2.blur(vert.reshape(-1, 1), (1, 5)).ravel() / max(1.0, np.median(vert))
    novo = cor[None] * np.clip(vert, 0.85, 1.15)[:, None, None]
    # borda suave (2 px) para não marcar a caixa
    msk = np.zeros((Y1 - Y0, X1 - X0), np.float32); msk[2:-2, 2:-2] = 1
    msk = cv2.GaussianBlur(msk, (5, 5), 0)[..., None]
    f[Y0:Y1, X0:X1] = np.clip(novo * msk + band * (1 - msk), 0, 255).astype(np.uint8)
    hh = y1 - y0
    fs = max(7, int(hh * a.alt / 0.72))
    fnt = ImageFont.truetype(FONT, fs)
    while fnt.getlength(a.texto) > (x1 - x0) * 0.95 and fs > 6:
        fs -= 1; fnt = ImageFont.truetype(FONT, fs)
    img = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)); d = ImageDraw.Draw(img)
    bb = fnt.getbbox(a.texto)
    d.text(((x0 + x1) / 2 - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), a.texto, font=fnt, fill=(236, 230, 212))
    f = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    p.stdin.write(f.tobytes()); n += 1
p.stdin.close(); p.wait(); print("ok", n)

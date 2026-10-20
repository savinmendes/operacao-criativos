# -*- coding: utf-8 -*-
"""Troca uma linha de legenda em CAIXA BRANCA com texto PRETO (estilo do vídeo 04).
Pinta de branco a caixa --caixa e escreve o texto novo centralizado, preto.
--ref: instante em que a legenda antiga está na tela; só troca quadros em que a caixa está igual (texto preto parecido).
  python trocar_legenda_caixa.py in.mp4 out.mp4 --de 175.3 --ate 178.6 --caixa x0,y0,x1,y1 --texto "..." [--px 22] [--ref 176]
"""
import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTES = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
ap = argparse.ArgumentParser()
ap.add_argument("entrada")
ap.add_argument("saida")
ap.add_argument("--de", type=float, required=True)
ap.add_argument("--ate", type=float, required=True)
ap.add_argument("--caixa", required=True)
ap.add_argument("--texto", required=True)
ap.add_argument("--px", type=int, default=0)
ap.add_argument("--fonte", default="Poppins-Medium.ttf")
ap.add_argument("--ref", type=float, default=None)
ap.add_argument("--base", type=int, default=None, help="linha de base do texto (y)")
a = ap.parse_args()
x0, y0, x1, y1 = map(int, a.caixa.split(","))
cap = cv2.VideoCapture(a.entrada)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
i0, i1 = int(round(a.de * fps)), int(round(a.ate * fps))
px = a.px or int((y1 - y0) * 0.62)
fonte = ImageFont.truetype(str(FONTES / a.fonte), px)
ref = None
if a.ref is not None:
    cr = cv2.VideoCapture(a.entrada)
    cr.set(cv2.CAP_PROP_POS_FRAMES, int(round(a.ref * fps)))
    _, rim = cr.read()
    ref = rim[y0:y1, x0:x1].max(2) < 90  # pixels pretos (letras)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", f"{fps}", "-i", "-", "-i", a.entrada, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                       "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", a.saida],
                      stdin=subprocess.PIPE)
i = n = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    if i0 <= i <= i1:
        mesmo = True
        if ref is not None:
            cur = im[y0:y1, x0:x1].max(2) < 90
            mesmo = (cur & ref).sum() / max(1, ref.sum()) > 0.5
        if mesmo:
            n += 1
            pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            d = ImageDraw.Draw(pil)
            bb = d.textbbox((0, 0), a.texto, font=fonte)
            tw = bb[2] - bb[0]
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            bx0, bx1 = min(x0, int(cx - tw / 2 - 8)), max(x1, int(cx + tw / 2 + 8))
            d.rounded_rectangle((bx0, y0, bx1, y1), radius=6, fill=(255, 255, 255))
            if a.base:
                d.text((cx, a.base), a.texto, font=fonte, fill=(0, 0, 0), anchor="ms")
            else:
                d.text((cx - tw / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), a.texto, font=fonte, fill=(0, 0, 0))
            im = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    ff.stdin.write(im.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print(f"ok: {a.saida} | {n} quadros trocados")

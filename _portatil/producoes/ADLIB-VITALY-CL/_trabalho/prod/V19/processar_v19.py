# -*- coding: utf-8 -*-
"""V19 suavizado: selo '114 KG'/'84 KG' -> 'ANTES'/'DESPUÉS' (mesmo tempo e lugar) e caixa da marca -> Lymphoria.
Áudio original copiado (só música). Duração igual ao original."""
import subprocess, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
V = r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\19 - Vitaly - 881380110992207.mp4"
FONT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Medium.ttf"
KG_TROCA = 247          # 1º quadro com '84 KG'
MARCA_INI = 445         # 1º quadro com 'Todo gracias a las gotas herbales de Vitaly'
def f(px): return ImageFont.truetype(FONT, px)
def tam_cap(cap, txt="H"):
    for s in range(10, 120):
        b = f(s).getbbox(txt)
        if b[3] - b[1] >= cap: return s
def tam_larg(txt, w):
    for s in range(10, 120):
        if f(s).getlength(txt) >= w: return s
KG_PX = tam_cap(33, "8")
MARCA_PX = tam_larg("Todo gracias a las gotas", 643 - 64)
print("fontes", KG_PX, MARCA_PX)
def caixa(im, cx, y0, y1, linhas, px, passo, min_box, pad=30, r=16):
    dr = ImageDraw.Draw(im); fo = f(px)
    w = max(fo.getlength(t) for t in linhas)
    x0, x1 = min(cx - w / 2 - pad, min_box[0]), max(cx + w / 2 + pad, min_box[2])
    x0, x1 = max(6, x0), min(714, x1)
    dr.rounded_rectangle((x0, min(y0, min_box[1]), x1, max(y1, min_box[3])), r, fill=(255, 255, 255))
    cap = fo.getbbox("H"); ch = cap[3] - cap[1]
    yt = (y0 + y1) / 2 - (passo * (len(linhas) - 1) + ch) / 2
    for k, t in enumerate(linhas):
        dr.text((cx - fo.getlength(t) / 2, yt + k * passo - cap[1]), t, font=fo, fill=(0, 0, 0))
cap = cv2.VideoCapture(V); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x1280", "-r", "30", "-i", "-",
                      "-i", V, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "15", "-threads", "3", "-pix_fmt", "yuv420p",
                      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-shortest",
                      "v19_suavizado_corpo.mp4"], stdin=subprocess.PIPE)
i = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
    caixa(im, 383, 877, 953, ["ANTES" if i < KG_TROCA else "DESPUÉS"], KG_PX, 0, (283, 877, 485, 953), pad=34, r=14)
    if i >= MARCA_INI:
        caixa(im, 360, 325, 465, ["Todo gracias a las gotas", "herbales de Lymphoria"], MARCA_PX, 59, (54, 325, 666, 465), pad=14, r=16)
    p.stdin.write(np.asarray(im).tobytes()); i += 1
p.stdin.close(); p.wait(); print("ok", i, "quadros")

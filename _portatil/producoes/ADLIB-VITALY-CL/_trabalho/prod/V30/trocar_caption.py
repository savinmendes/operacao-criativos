# -*- coding: utf-8 -*-
"""Troca a última linha da legenda branca ('Vitaly') por 'Lymphoria' (caixa branca opaca + texto preto),
só nos quadros em que a caixa original está na tela."""
import subprocess, sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ent, sai = sys.argv[1], sys.argv[2]
F = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-SemiBold.ttf"
cap = cv2.VideoCapture(ent); fps = cap.get(5); W, H = int(cap.get(3)), int(cap.get(4))
fonte = ImageFont.truetype(F, 47)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-c:a", "copy", "-threads", "3", sai], stdin=subprocess.PIPE)
i = n = 0
while True:
    ok, im = cap.read()
    if not ok: break
    # caixa branca da linha "Vitaly": bordas brancas fora das letras
    reg = im[935:975, 160:190].min(2)
    if (reg > 225).mean() > 0.9:
        pil = Image.fromarray(im[..., ::-1].copy()); d = ImageDraw.Draw(pil)
        d.rounded_rectangle((128, 919, 427, 980), 14, fill=(255, 255, 255))
        d.rectangle((128, 919, 427, 935), fill=(255, 255, 255))
        d.text((277.5, 948), "Lymphoria", font=fonte, fill=(0, 0, 0), anchor="mm")
        im = np.asarray(pil)[..., ::-1].copy(); n += 1
    ff.stdin.write(im.tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok", i, "quadros,", n, "trocados")

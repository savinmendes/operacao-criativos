# -*- coding: utf-8 -*-
"""título do gancho P7 (estilo v3/final_B/titulo.py)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
AQ = Path(__file__).resolve().parent; G = Path(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\graficos")
L1, L2 = "LO HUMILLARON POR SU FE…", "DÍAS DESPUÉS PASÓ ESTO"
f = ImageFont.truetype(str(G / "Poppins-ExtraBold.ttf"), 33)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
R = 13; gap = 12
w1 = d.textlength(L1, font=f) + 2 * R + gap; w2 = d.textlength(L2, font=f); W = max(w1, w2) + 40
x0 = (720 - W) / 2; y0 = 297 + 10; H = 104
d.rounded_rectangle([x0, y0, x0 + W, y0 + H], radius=14, fill=(0, 0, 0, 236), outline=(230, 30, 30, 255), width=3)
xa = (720 - w1) / 2; cy = y0 + 30
d.ellipse([xa, cy - R, xa + 2 * R, cy + R], fill=(235, 25, 25, 255))
d.text((xa + 2 * R + gap, cy), L1, font=f, fill=(255, 255, 255, 255), anchor="lm")
d.text((360, y0 + 74), L2, font=f, fill=(255, 221, 0, 255), anchor="mm")
im.save(AQ / "titulo_gancho.png"); print("ok", W)

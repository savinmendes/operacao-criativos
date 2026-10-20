# -*- coding: utf-8 -*-
"""header feminino da moldura do post + título do gancho (estilo titulo.py da v4 B)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
AQ = Path(__file__).resolve().parent; G = AQ.parents[2] / "_trabalho" / "graficos"; O = AQ / "graficos"
def P(peso, t): return ImageFont.truetype(str(G / f"Poppins-{peso}.ttf"), t)
def caber(d, txt, peso, tam, maxw):
    while d.textlength(txt, font=P(peso, tam)) > maxw and tam > 8: tam -= 0.5
    return P(peso, tam)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rectangle([145, 146, 648, 197], fill=(251, 251, 251, 255)); d.rectangle([145, 197, 715, 238], fill=(251, 251, 251, 255))
d.text((156, 186), "Fe en Noticias", font=caber(d, "Fe en Noticias", "SemiBold", 40, 252), fill=(11, 11, 11, 255), anchor="ls")
t = "Trabajadora es humillada y algo impactante sucede"
d.text((153, 223), t, font=caber(d, t, "Medium", 26, 520), fill=(22, 22, 22, 255), anchor="ls")
im.save(O / "header_f.png")
L1, L2 = "LA HUMILLARON EN SU SALÓN…", "AL DÍA SIGUIENTE PASÓ ESTO"
f = P("ExtraBold", 33)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
R = 13; gap = 12
w1 = d.textlength(L1, font=f) + 2 * R + gap; w2 = d.textlength(L2, font=f); W = max(w1, w2) + 40
x0 = (720 - W) / 2; y0 = 297 + 10; H = 104
d.rounded_rectangle([x0, y0, x0 + W, y0 + H], radius=14, fill=(0, 0, 0, 236), outline=(230, 30, 30, 255), width=3)
xa = (720 - w1) / 2; cy = y0 + 30
d.ellipse([xa, cy - R, xa + 2 * R, cy + R], fill=(235, 25, 25, 255))
d.text((xa + 2 * R + gap, cy), L1, font=f, fill=(255, 255, 255, 255), anchor="lm")
d.text((360, y0 + 74), L2, font=f, fill=(255, 221, 0, 255), anchor="mm")
im.save(O / "titulo_gancho.png"); print("ok", W)

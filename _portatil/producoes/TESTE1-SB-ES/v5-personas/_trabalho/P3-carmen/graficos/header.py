# -*- coding: utf-8 -*-
"""header do post (feminino) — mesmo desenho do _trabalho/graficos/gerar.py header()"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
AQ = Path(__file__).resolve().parent; G = Path(r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\graficos")
def P(peso, t): return ImageFont.truetype(str(G / f"Poppins-{peso}.ttf"), t)
def caber(d, txt, fn, tam, maxw):
    while d.textlength(txt, font=fn(tam)) > maxw and tam > 8: tam -= 0.5
    return fn(tam)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rectangle([145, 146, 648, 197], fill=(251, 251, 251, 255)); d.rectangle([145, 197, 715, 238], fill=(251, 251, 251, 255))
ft = caber(d, "Fe en Noticias", lambda s: P("SemiBold", s), 40, 252)
d.text((156, 186), "Fe en Noticias", font=ft, fill=(11, 11, 11, 255), anchor="ls")
t = "Trabajadora es humillada y algo impactante sucede"
fs = caber(d, t, lambda s: P("Medium", s), 26, 520)
d.text((153, 223), t, font=fs, fill=(22, 22, 22, 255), anchor="ls")
im.save(AQ / "header.png"); print("ok")

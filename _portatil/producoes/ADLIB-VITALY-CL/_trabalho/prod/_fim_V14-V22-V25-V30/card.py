# -*- coding: utf-8 -*-
"""Card da oferta: 2 frascos (recorte da foto kit3) + faixa "COMPRE 1, RECIBA 2 · $34.990"."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
K = r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad04\kit3_quadrado.jpg"
F = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts"
im = Image.open(K).convert("RGB")
S = 1600
dois = im.crop((10, 0, 1022, 1600))                       # 2 frascos da esquerda
bg = im.resize((S, S)).filter(ImageFilter.GaussianBlur(30))
c = Image.new("RGB", (S, S)); c.paste(bg)
d2 = dois.resize((int(1012 * 0.86), int(1600 * 0.86)), Image.LANCZOS)
c.paste(d2, ((S - d2.width) // 2, 0))
d = ImageDraw.Draw(c)
y0 = 1180
d.rounded_rectangle((90, y0, S - 90, y0 + 330), 40, fill=(22, 74, 48))
f1 = ImageFont.truetype(F + r"\Poppins-Bold.ttf", 128)
f2 = ImageFont.truetype(F + r"\Poppins-Bold.ttf", 96)
for txt, f, y, cor in [("COMPRE 1, RECIBA 2", f1, y0 + 95, (255, 255, 255)), ("$34.990 · ENVÍO GRATIS", f2, y0 + 245, (255, 214, 0))]:
    w = d.textlength(txt, font=f)
    d.text(((S - w) / 2, y), txt, font=f, fill=cor, anchor="lm")
c.save("card_oferta.jpg", quality=95)
print("ok")

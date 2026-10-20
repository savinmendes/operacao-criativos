# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
W, H = 720, 1280
F = r"C:\Windows\Fonts\segoeui.ttf"; FB = r"C:\Windows\Fonts\segoeuib.ttf"; FE = r"C:\Windows\Fonts\seguiemj.ttf"
im = Image.new("RGB", (W, H), (236, 229, 221)); d = ImageDraw.Draw(im)
# textura leve do fundo
import random; random.seed(4)
for _ in range(900):
    x, y = random.randrange(W), random.randrange(H); d.point((x, y), fill=(226, 218, 208))
# barra de status + cabeçalho
d.rectangle([0, 0, W, 44], fill=(0, 94, 84)); d.text((24, 8), "18:47", font=ImageFont.truetype(FB, 24), fill="white")
d.text((W - 120, 8), "4G  83%", font=ImageFont.truetype(FB, 22), fill="white")
d.rectangle([0, 44, W, 150], fill=(0, 128, 105))
d.text((22, 70), "←", font=ImageFont.truetype(FB, 40), fill="white")
d.ellipse([70, 62, 136, 128], fill=(200, 160, 170)); d.text((88, 70), "C", font=ImageFont.truetype(FB, 40), fill="white")
fn = ImageFont.truetype(FB, 32); fe = ImageFont.truetype(FE, 28)
d.text((152, 64), "Mi amor", font=fn, fill="white")
w_ = d.textlength("Mi amor ", font=fn); d.text((152 + w_, 70), "❤️", font=fe, embedded_color=True)
d.text((152, 104), "en línea", font=ImageFont.truetype(F, 24), fill=(220, 240, 235))
# etiqueta de data
fs = ImageFont.truetype(F, 22); t = "HOY"; tw = d.textlength(t, font=fs)
d.rounded_rectangle([W/2 - tw/2 - 16, 360, W/2 + tw/2 + 16, 396], 10, fill=(225, 243, 251)); d.text((W/2 - tw/2, 364), t, font=fs, fill=(80, 90, 95))
# mensagem anterior dele (saída) e a dela (entrada)
fm = ImageFont.truetype(F, 34); fem = ImageFont.truetype(FE, 30)
def bolha(y, partes, sai, hora):
    larg = sum(d.textlength(p, font=(fem if e else fm)) for p, e in partes)
    bw = larg + 40 + 90; x0 = W - 24 - bw if sai else 24
    cor = (220, 248, 198) if sai else (255, 255, 255)
    d.rounded_rectangle([x0, y, x0 + bw, y + 92], 16, fill=cor)
    x = x0 + 20
    for p, e in partes:
        if e: d.text((x, y + 22), p, font=fem, embedded_color=True)
        else: d.text((x, y + 16), p, font=fm, fill=(17, 27, 33))
        x += d.textlength(p, font=(fem if e else fm))
    d.text((x0 + bw - 80, y + 58), hora + (" ✓✓" if sai else ""), font=ImageFont.truetype(F, 20), fill=(83, 189, 235) if sai else (120, 130, 135))

y = 430
d.rounded_rectangle([24, y, 690, y + 140], 16, fill="white")
d.text((44, y + 16), "Mañana vienen mis papás", font=fm, fill=(17, 27, 33))
d.text((44, y + 62), "al asado ", font=fm, fill=(17, 27, 33))
x = 44 + d.textlength("al asado ", font=fm)
d.text((x, y + 68), "😊❤️", font=fem, embedded_color=True)
d.text((620, y + 106), "18:47", font=ImageFont.truetype(F, 20), fill=(120, 130, 135))
# barra de digitação
d.rectangle([0, H - 110, W, H], fill=(236, 229, 221)); d.rounded_rectangle([16, H - 96, W - 110, H - 24], 36, fill="white")
d.text((50, H - 82), "Mensaje", font=ImageFont.truetype(F, 30), fill=(140, 150, 155))
d.ellipse([W - 92, H - 100, W - 16, H - 24], fill=(0, 168, 132))
im.save("cenas/S0_whatsapp.png"); print("ok")

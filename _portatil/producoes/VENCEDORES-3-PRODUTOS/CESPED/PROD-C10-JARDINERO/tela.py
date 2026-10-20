# -*- coding: utf-8 -*-
"""Telas de WhatsApp (estilo genérico, sem logo) feitas por código para o C10.
Gera cenas/tela_g1..g3.png (gancho: 1, 2 e 3 mensagens iguais do jardineiro) e cenas/tela_v.png (virada: resposta dele).
Cada PNG é um cartão de celular RGBA 640 px de largura, para sobrepor sobre a cena desfocada."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

P = Path(__file__).parent / "cenas"; P.mkdir(exist_ok=True)
F = "C:/Windows/Fonts/"
f_nome = ImageFont.truetype(F + "segoeuib.ttf", 34)
f_sub = ImageFont.truetype(F + "segoeui.ttf", 24)
f_msg = ImageFont.truetype(F + "segoeui.ttf", 33)
f_hora = ImageFont.truetype(F + "segoeui.ttf", 21)
f_data = ImageFont.truetype(F + "segoeuib.ttf", 21)
f_emo = ImageFont.truetype(F + "seguiemj.ttf", 33)

W, H = 640, 1000
VERDE, FUNDO, BRANCO, SAIDA = (0, 128, 105), (236, 229, 221), (255, 255, 255), (217, 253, 211)
MSG = "Don, esta semana tampoco puedo ir"
EMO = "🙏"
RESP = "No se preocupe, Don Lalo. Ya no lo necesito"
EMO_R = "😎"


def texto_com_emoji(d, x, y, txt, emo, cor=(17, 27, 33)):
    d.text((x, y), txt, font=f_msg, fill=cor)
    w = d.textlength(txt + " ", font=f_msg)
    d.text((x + w, y + 3), emo, font=f_emo, embedded_color=True)


def quebra(txt, emo, maxw, d):
    pal, linhas, cur = txt.split(), [], ""
    for p in pal:
        t = (cur + " " + p).strip()
        if d.textlength(t + " " + emo, font=f_msg) > maxw and cur:
            linhas.append(cur); cur = p
        else:
            cur = t
    linhas.append(cur)
    return linhas


def bolha(im, d, y, txt, emo, hora, saida=False):
    maxw = 440
    linhas = quebra(txt, emo, maxw, d)
    larg = max(d.textlength(l + (" " + emo if i == len(linhas) - 1 else ""), font=f_msg) + (36 if i == len(linhas) - 1 else 0)
               for i, l in enumerate(linhas))
    bw = int(larg) + 36 + 70
    bh = 22 + 42 * len(linhas) + 26
    x = W - bw - 22 if saida else 22
    d.rounded_rectangle([x, y, x + bw, y + bh], 18, fill=SAIDA if saida else BRANCO)
    for i, l in enumerate(linhas):
        if i == len(linhas) - 1:
            texto_com_emoji(d, x + 18, y + 12 + 42 * i, l, emo)
        else:
            d.text((x + 18, y + 12 + 42 * i), l, font=f_msg, fill=(17, 27, 33))
    hx = x + bw - (100 if saida else 70)
    d.text((hx, y + bh - 32), hora, font=f_hora, fill=(102, 119, 129))
    if saida:  # dois tiques azuis
        cx, cy = x + bw - 36, y + bh - 20
        for o in (0, 9):
            d.line([(cx + o - 8, cy), (cx + o - 3, cy + 5), (cx + o + 7, cy - 6)], fill=(83, 189, 235), width=3)
    return y + bh + 14


def data(d, y, txt):
    w = d.textlength(txt, font=f_data) + 30
    d.rounded_rectangle([(W - w) / 2, y, (W + w) / 2, y + 38], 10, fill=(255, 255, 255))
    d.text(((W - w) / 2 + 15, y + 6), txt, font=f_data, fill=(84, 101, 111))
    return y + 54


def cartao(itens):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base = Image.new("RGBA", (W, H), FUNDO + (255,))
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, W, 120], fill=VERDE)
    d.ellipse([70, 26, 138, 94], fill=(190, 200, 205))
    d.ellipse([92, 38, 116, 62], fill=(240, 240, 240)); d.pieslice([78, 62, 130, 112], 180, 360, fill=(240, 240, 240))
    d.line([(26, 60), (44, 44)], fill="white", width=4); d.line([(26, 60), (44, 76)], fill="white", width=4)
    d.text((156, 26), "Jardinero Don Lalo", font=f_nome, fill="white")
    d.text((156, 70), "en línea", font=f_sub, fill=(220, 240, 235))
    y = 150
    for it in itens:
        if it[0] == "data":
            y = data(d, y, it[1])
        else:
            y = bolha(base, d, y, it[1], it[2], it[3], it[0] == "out")
    # rodapé de digitação
    d.rounded_rectangle([16, H - 84, W - 96, H - 22], 31, fill="white")
    d.text((44, H - 70), "Mensaje", font=f_msg, fill=(140, 150, 155))
    d.ellipse([W - 84, H - 86, W - 18, H - 20], fill=VERDE)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 44, fill=255)
    im.paste(base, (0, 0), mask)
    # moldura
    ImageDraw.Draw(im).rounded_rectangle([0, 0, W - 1, H - 1], 44, outline=(25, 25, 25), width=10)
    return im


s1 = [("data", "LUNES 29 DE SEPT."), ("in", MSG, EMO, "08:12")]
s2 = s1 + [("data", "LUNES 6 DE OCT."), ("in", MSG, EMO, "08:05")]
s3 = s2 + [("data", "HOY"), ("in", MSG, EMO, "08:09")]
for n, s in (("g1", s1), ("g2", s2), ("g3", s3)):
    cartao(s).save(P / f"tela_{n}.png")
cartao([("data", "HOY"), ("in", MSG, EMO, "08:09"), ("out", RESP, EMO_R, "18:40")]).save(P / "tela_v.png")
print("ok")

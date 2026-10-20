# -*- coding: utf-8 -*-
"""Prints de WhatsApp em espanhol (conversas genéricas, nomes inventados, sem telefone). 720 px de largura."""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path(__file__).resolve().parent
F = "C:/Windows/Fonts/"
def f(n, s): return ImageFont.truetype(F + n, s)
TX, TXB, HORA, EMO = f("segoeui.ttf", 27), f("seguisb.ttf", 30), f("segoeui.ttf", 18), f("seguiemj.ttf", 34)
EMO_RE = re.compile("([\U0001F300-\U0001FAFF\u2600-\u27BF\u2728\u2764]\ufe0f?)")
def larg(t):
    return sum((EMO.getlength(p) if EMO_RE.fullmatch(p) else TX.getlength(p)) for p in EMO_RE.split(t) if p)
def quebra(t, w):
    out, cur = [], ""
    for pal in t.split(" "):
        tt = (cur + " " + pal).strip()
        if larg(tt) <= w: cur = tt
        else: out.append(cur); cur = pal
    out.append(cur); return out
def texto(d, im, x, y, t):
    for p in EMO_RE.split(t):
        if not p: continue
        if EMO_RE.fullmatch(p):
            d.text((x, y - 4), p, font=EMO, embedded_color=True); x += EMO.getlength(p)
        else:
            d.text((x, y), p, font=TX, fill=(17, 27, 33)); x += TX.getlength(p)
CHATS = {
 "wa1": ("Lucía Paredes", (214, 120, 90), [
    ("in", "Padre Juan, bendición 🙏", "07:48"),
    ("in", "Recé la oración de San Benito con usted y sentí una paz enorme", "07:49"),
    ("in", "Hoy me llamaron para la entrevista que estaba esperando 😭🙌", "07:50"),
    ("out", "Gloria a Dios, Lucía. Sigue firme en la fe 🙏", "08:22"),
    ("in", "Amén padre, ya lo compartí con mi familia ❤️", "08:23")]),
 "wa2": ("Ana Beatriz", (96, 140, 200), [
    ("in", "Padre, gracias por enseñar la oración en vivo", "09:14"),
    ("in", "Mi jefe me trataba muy mal... y hoy me ofrecieron un trabajo mejor!! 🙌", "09:15"),
    ("in", "Todavía no lo puedo creer 🙏✨", "09:15"),
    ("out", "Qué bendición, Ana. San Benito te acompaña", "09:40"),
    ("in", "Gracias padre ❤️", "09:41")]),
 "wa3": ("Gloria Ramírez", (150, 110, 180), [
    ("in", "Padre Juan, le escribo para contarle 🙏", "10:02"),
    ("in", "Después de rezar con usted, en mi casa volvió la tranquilidad", "10:03"),
    ("in", "Le mandé el video a mis hermanas y a mi mamá ❤️", "10:04"),
    ("out", "Dios bendiga tu hogar, Gloria 🙏", "10:31")]),
}
W = 720
for nome, (pessoa, cor, msgs) in CHATS.items():
    H = 1180; im = Image.new("RGB", (W, H), (239, 234, 226)); d = ImageDraw.Draw(im)
    # padrão discreto do fundo
    for yy in range(140, H, 46):
        for xx in range((yy // 46 % 2) * 23, W, 46): d.ellipse((xx, yy, xx + 3, yy + 3), fill=(229, 223, 213))
    # cabeçalho
    d.rectangle((0, 0, W, 128), fill=(255, 255, 255)); d.line((0, 128, W, 128), fill=(220, 220, 220), width=2)
    d.text((26, 64), "‹", font=f("segoeui.ttf", 60), fill=(0, 128, 105), anchor="lm")
    d.ellipse((66, 34, 126, 94), fill=cor); d.text((96, 64), pessoa[0], font=f("seguisb.ttf", 32), fill=(255, 255, 255), anchor="mm")
    d.text((144, 46), pessoa, font=TXB, fill=(17, 27, 33)); d.text((144, 84), "en línea", font=f("segoeui.ttf", 21), fill=(102, 119, 129))
    y = 170
    for lado, t, h in msgs:
        mw = 470; ls = quebra(t, mw); tw = max(larg(l) for l in ls); bw = int(max(tw, 90) + 36 + 60); bh = 18 + len(ls) * 37 + 20
        x0 = 24 if lado == "in" else W - 24 - bw
        d.rounded_rectangle((x0, y, x0 + bw, y + bh), 16, fill=(255, 255, 255) if lado == "in" else (217, 253, 211))
        for k, l in enumerate(ls): texto(d, im, x0 + 18, y + 14 + k * 37, l)
        hx = x0 + bw - 14; d.text((hx - (22 if lado == "out" else 0), y + bh - 10), h, font=HORA, fill=(102, 119, 129), anchor="rs")
        if lado == "out": d.text((hx, y + bh - 10), "✓✓", font=f("seguisym.ttf", 17), fill=(83, 189, 235), anchor="rs")
        y += bh + 16
    im = im.crop((0, 0, W, max(y + 30, 900))); im.save(P / f"{nome}.png"); print(nome, im.size)

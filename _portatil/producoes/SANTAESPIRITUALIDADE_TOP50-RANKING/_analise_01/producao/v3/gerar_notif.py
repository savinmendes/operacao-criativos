# -*- coding: utf-8 -*-
"""Celular cheio de mensagens (tela de bloqueio com notificações empilhadas; nomes inventados, sem telefone, sem marca).
Gera v3/notif.png (720 x ~2200) para rolar no b-roll «testimonios… no mienten»."""
import re, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent
F = "C:/Windows/Fonts/"
def f(n, s): return ImageFont.truetype(F + n, s)
TT, TX, HR, EMO = f("seguisb.ttf", 27), f("segoeui.ttf", 25), f("segoeui.ttf", 20), f("seguiemj.ttf", 28)
EMO_RE = re.compile("([\U0001F300-\U0001FAFF\u2600-\u27BF\u2728\u2764]\ufe0f?)")
MSG = [
 ("Rosa Elena", "Padre, recé con usted y hoy me llamaron del trabajo", "ahora"),
 ("Carmen Lucía", "Mi esposo y yo volvimos a hablarnos. Gracias, padre", "1 min"),
 ("Don Ernesto", "Pagué la deuda que tenía hace dos años", "2 min"),
 ("María Fernanda", "Le mandé el video a toda mi familia", "3 min"),
 ("Luz Marina", "Mi hijo consiguió trabajo después de 8 meses", "4 min"),
 ("Jorge Alberto", "Gracias, padre Juan. Bendiciones", "5 min"),
 ("Teresa", "Amanecí con una paz que no sentía hace años", "6 min"),
 ("Gloria Inés", "Mi negocio volvió a tener clientes", "7 min"),
 ("Ana Lucía", "¿A qué hora vuelve a rezar en vivo?", "8 min"),
 ("Patricia", "Recé con fe y todo empezó a cambiar", "9 min"),
 ("Don Ramiro", "Dios lo bendiga, padre", "10 min"),
 ("Silvia", "Ya se lo pasé a mis hermanas", "12 min"),
]
COR = [(214, 120, 90), (90, 130, 200), (120, 90, 170), (60, 150, 120), (200, 90, 120), (210, 160, 60)]
def larg(t, ft): return sum((EMO.getlength(p) if EMO_RE.fullmatch(p) else ft.getlength(p)) for p in EMO_RE.split(t) if p)
def escreve(d, x, y, t, ft, cor):
    for p in EMO_RE.split(t):
        if not p: continue
        if EMO_RE.fullmatch(p): d.text((x, y - 3), p, font=EMO, embedded_color=True); x += EMO.getlength(p)
        else: d.text((x, y), p, font=ft, fill=cor); x += ft.getlength(p)
def quebra(t, w):
    out, cur = [], ""
    for pal in t.split(" "):
        tt = (cur + " " + pal).strip()
        if larg(tt, TX) <= w: cur = tt
        else: out.append(cur); cur = pal
    out.append(cur); return out
CH = 132; GAP = 14; TOP = 230
H = TOP + len(MSG) * (CH + GAP) + 400
# fundo: gradiente roxo-azulado desfocado (papel de parede genérico)
yy = np.linspace(0, 1, H)[:, None]; xx = np.linspace(0, 1, 720)[None]
bg = np.dstack([np.broadcast_to(c, (H, 720)) for c in (40 + 60 * xx * (1 - yy), 30 + 40 * yy + 0 * xx, 80 + 90 * (1 - yy) * (1 - xx * .4))]).clip(0, 255).astype(np.uint8)
im = Image.fromarray(bg).convert("RGBA"); d = ImageDraw.Draw(im)
for i, (nm, msg, hr) in enumerate(MSG):
    y = TOP + i * (CH + GAP)
    card = Image.new("RGBA", (680, CH), (0, 0, 0, 0)); dc = ImageDraw.Draw(card)
    dc.rounded_rectangle((0, 0, 679, CH - 1), 26, fill=(245, 245, 247, 236))
    dc.rounded_rectangle((20, 24, 70, 74), 12, fill=(37, 180, 90, 255))                     # ícone genérico de chat (sem marca)
    dc.ellipse((31, 34, 59, 60), fill=(255, 255, 255, 255)); dc.polygon([(36, 56), (33, 66), (44, 59)], fill=(255, 255, 255, 255))
    dc.text((88, 30), nm, font=TT, fill=(20, 20, 20, 255), anchor="lm"); dc.text((660, 30), hr, font=HR, fill=(110, 110, 115, 255), anchor="rm")
    ls = quebra(msg, 560)[:2]
    for k, l in enumerate(ls): escreve(dc, 88, 52 + k * 32, l, TX, (40, 40, 45, 255))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.putalpha(card.split()[3].point(lambda v: int(v * .25)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (20, y + 4)); im.alpha_composite(card, (20, y))
im.convert("RGB").save(P / "notif.png"); print(im.size)

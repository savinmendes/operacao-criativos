# -*- coding: utf-8 -*-
"""Lote 2 de estáticos Pellorini: todas as estratégias do estudo das 11 lojas (custo zero, fotos da loja).

python gerar_lote2.py            -> lote2/<familia>/<conceito>_<persona>_<familia>_<produto>_<fmt>.jpg + folhas de revisão
Famílias e referência no estudo estão na docstring de cada função.
"""
import json
import os
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

from gerar_lote import (BASE, CREAM, F, FOTOS, FORMATOS, GOLD, GREEN, INK, MARCA, RED, colar_relogio, fonte, foto,
                        fundo, icone, marca, pilula, texto_c)

SAIDA = os.path.join(BASE, "lote2")
CLASS = json.load(open(os.path.join(BASE, "classificacao.json"), encoding="utf-8"))
WHITE = (255, 255, 255)
random.seed(7)


def mao(tam):
    return ImageFont.truetype(os.path.join(F, "PermanentMarker.ttf"), tam)


def caveat(tam):
    f = ImageFont.truetype(os.path.join(F, "Caveat.ttf"), tam)
    try:
        f.set_variation_by_axes([700])
    except Exception:
        pass
    return f


def nome_curto(handle):
    return handle.replace("pelvini-", "").replace("-1", "").replace("-limited-edition", "").replace("-", " ").title()


def abrir(nome):
    return Image.open(os.path.join(FOTOS, nome)).convert("RGB")


def recorte(handle, n=1):
    """Recorta a foto de fundo preto: fundo = região escura ligada às bordas."""
    im = foto(handle, n)
    a = np.asarray(im.convert("L")).astype(np.int16)
    escuro = a < 22
    rot, _ = ndimage.label(escuro)
    bordas = set(np.unique(np.concatenate([rot[0], rot[-1], rot[:, 0], rot[:, -1]]))) - {0}
    fundo_m = np.isin(rot, list(bordas))
    alpha = Image.fromarray(((~fundo_m) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba.crop(alpha.getbbox())


def colar_rgba(dest, rgba, cx, cy, alt, sombra=True):
    r = alt / rgba.height
    im = rgba.resize((max(1, int(rgba.width * r)), int(alt)), Image.LANCZOS)
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    if sombra:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(im.getchannel("A").point(lambda v: int(v * 0.35)))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        dest.paste(sh, (x + 10, y + 22), sh)
    dest.paste(im, (x, y), im)


def cobrir(im, w, h, foco=0.5):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = int((im.width - w) * 0.5)
    y = int((im.height - h) * foco)
    return im.crop((x, y, x + w, y + h))


def degrade_baixo(im, ini=0.55, forca=235):
    w, h = im.size
    g = Image.linear_gradient("L").resize((w, h))
    g = g.point(lambda v: 0 if v < ini * 255 else int((v - ini * 255) / (255 - ini * 255) * forca))
    preto = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(preto, im, g)


def quebrar(d, txt, f, larg):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if d.textlength(t, font=f) <= larg:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    linhas.append(atual)
    return linhas


def cor_mostrador(handle):
    im = foto(handle).resize((60, 60))
    c = np.asarray(im)[22:36, 22:38].reshape(-1, 3).mean(0)
    return tuple(int(v) for v in c)


def eh_alto(fmt):
    return fmt == "9x16"


# ======================= famílias com recorte (fundo claro/colorido) =======================

def f_bogo_saturado(fmt, principal, brinde, bg=(242, 107, 29)):
    """AlphaGear 001/002: fundo saturado, FREE gigante, produto + brinde menor, 'ONLY TODAY · NO CODE NEEDED'."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 60 if not a else 140, "BUY 1 · GET 1", fonte("anton", 92 if not a else 120), INK)
    texto_c(d, w, 150 if not a else 270, "FREE", fonte("anton", 300 if not a else 380), WHITE)
    cy = 730 if not a else 1290
    colar_rgba(im, recorte(principal), w * 0.34, cy, 430 if not a else 660)
    colar_rgba(im, recorte(brinde), w * 0.72, cy + 30, 340 if not a else 520)
    d = ImageDraw.Draw(im)
    sx, sy = int(w * 0.88), int(cy - (120 if not a else 200))
    d.ellipse((sx - 85, sy - 85, sx + 85, sy + 85), fill=INK)
    d.text((sx - d.textlength("FREE", font=fonte("anton", 60)) / 2, sy - 40), "FREE", font=fonte("anton", 60), fill=bg)
    d.rectangle((0, h - (110 if not a else 170), w, h), fill=INK)
    texto_c(d, w, h - (80 if not a else 120), "ONLY TODAY  ·  NO CODE NEEDED", fonte("sans", 36 if not a else 42, 800), WHITE, espaco=2)
    return im


def f_is_name_worth(fmt, prod):
    """Laphont 010/031: off-white, serif itálico, setas à mão, sem desconto."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (244, 239, 230))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    fs = fonte("serif", 80 if not a else 92, 500)
    y = 70 if not a else 150
    for l in ["Is a name worth", "$4,000?"]:
        texto_c(d, w, y, l, fs, INK)
        y += 100 if not a else 115
    cy = 640 if not a else 1100
    colar_rgba(im, recorte(prod), w * 0.62, cy, 560 if not a else 820)
    d = ImageDraw.Draw(im)
    fx = caveat(46 if not a else 54)
    notas = ["316L steel", "sapphire crystal", "2-year warranty", "no logo tax"]
    yy = cy - (190 if not a else 280)
    for t in notas:
        d.text((60, yy), t, font=fx, fill=(40, 36, 32))
        d.line((60 + d.textlength(t, font=fx) + 14, yy + 32, w * 0.62 - 150, cy - 40 + random.randint(-60, 60)), fill=(40, 36, 32), width=3)
        yy += 110 if not a else 150
    texto_c(d, w, h - (90 if not a else 160), MARCA, fonte("sans", 30, 600), (60, 56, 50), espaco=14)
    return im


def f_vs_designer(fmt, prod):
    """Monomods 002/006: VS de preço, sem foto nem nome de marca de luxo."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h, (30, 30, 30), (8, 8, 8))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 50 if not a else 120, "Why pay for the name?", fonte("serif", 70 if not a else 84, 600), CREAM)
    top = 170 if not a else 330
    alt = 600 if not a else 980
    d.rounded_rectangle((40, top, w / 2 - 30, top + alt), radius=24, fill=(52, 50, 48))
    d.rounded_rectangle((w / 2 + 30, top, w - 40, top + alt), radius=24, fill=(18, 17, 16), outline=GOLD, width=3)
    cx1 = (40 + w / 2 - 30) / 2
    texto_c_x(d, cx1, top + 60, "DESIGNER", fonte("anton", 64), (150, 146, 140))
    texto_c_x(d, cx1, top + 135, "BRAND", fonte("anton", 64), (150, 146, 140))
    fp = fonte("anton", 110 if not a else 140)
    pt = "$4,000+"
    py = top + alt / 2 - 40
    texto_c_x(d, cx1, py, pt, fp, (190, 186, 180))
    lw = d.textlength(pt, font=fp)
    d.line((cx1 - lw / 2 - 10, py + 80, cx1 + lw / 2 + 10, py + 50), fill=RED, width=10)
    texto_c_x(d, cx1, top + alt - 110, "you pay for the logo", caveat(48), (170, 166, 160))
    cx2 = (w / 2 + 30 + w - 40) / 2
    colar_relogio(im, foto(prod), cx2, top + alt * 0.45, alt * 0.72)
    d = ImageDraw.Draw(im)
    texto_c_x(d, cx2, top + alt - 120, MARCA, fonte("sans", 30, 700), GOLD, 8)
    texto_c_x(d, cx2, top + alt - 75, "2nd watch FREE", fonte("sans", 30, 600), CREAM)
    d.ellipse((w / 2 - 55, top + alt / 2 - 55, w / 2 + 55, top + alt / 2 + 55), fill=GOLD)
    texto_c_x(d, w / 2, top + alt / 2 - 36, "VS", fonte("anton", 56), INK)
    y = top + alt + (40 if not a else 90)
    for t in ["2-year warranty", "90-day returns", "Free worldwide shipping"] if a else ["2-year warranty  ·  90-day returns  ·  Free shipping"]:
        texto_c(d, w, y, t, fonte("sans", 30 if not a else 38, 600), (210, 204, 194))
        y += 60
    return im


def texto_c_x(d, cx, y, txt, f, cor, espaco=0):
    if espaco:
        larg = sum(d.textlength(c, font=f) for c in txt) + espaco * (len(txt) - 1)
        x = cx - larg / 2
        for c in txt:
            d.text((x, y), c, font=f, fill=cor)
            x += d.textlength(c, font=f) + espaco
        return
    d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=cor)


def f_qual_voce(fmt, a_, b_, la, lb, titulo="Which one are you?"):
    """AlphaGear 039 '¿Qué prefieres?': fundo branco dividido, 2 produtos e rótulos."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    d.rectangle((w / 2, 0, w, h), fill=(240, 236, 228))
    texto_c(d, w, 50 if not a else 140, titulo, fonte("serif", 72 if not a else 86, 600), INK)
    cy = 560 if not a else 1000
    colar_rgba(im, recorte(a_), w * 0.25, cy, 560 if not a else 860)
    colar_rgba(im, recorte(b_), w * 0.75, cy, 560 if not a else 860)
    d = ImageDraw.Draw(im)
    yl = 900 if not a else 1530
    texto_c_x(d, w * 0.25, yl, la, fonte("anton", 64 if not a else 76), INK)
    texto_c_x(d, w * 0.75, yl, lb, fonte("anton", 64 if not a else 76), INK)
    texto_c(d, w, h - (70 if not a else 200), "Can't choose? Get both: the 2nd one is FREE", fonte("sans", 30 if not a else 36, 700), (120, 90, 40))
    return im


def f_ranking(fmt, prods, titulo):
    """AlphaGear 041 'TOP 4 ...': lista numerada com os modelos."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (246, 241, 233))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    linhas = quebrar(d, titulo, fonte("serif", 64 if not a else 80, 600), w - 120)
    y = 50 if not a else 120
    for l in linhas:
        texto_c(d, w, y, l, fonte("serif", 64 if not a else 80, 600), INK)
        y += 78 if not a else 96
    cols = 2
    top = y + 20
    ch = (h - top - (60 if not a else 160)) / 2
    cw = w / 2
    for i, p in enumerate(prods[:4]):
        cx, cy = cw * (i % 2) + cw / 2, top + ch * (i // 2) + ch / 2
        colar_rgba(im, recorte(p), cx + 20, cy - ch * 0.04, ch * 0.86)
        d = ImageDraw.Draw(im)
        d.ellipse((cx - cw / 2 + 30, cy - ch / 2 + 20, cx - cw / 2 + 110, cy - ch / 2 + 100), fill=INK)
        texto_c_x(d, cx - cw / 2 + 70, cy - ch / 2 + 32, str(i + 1), fonte("anton", 48), GOLD)
        texto_c_x(d, cx + 20, cy + ch * 0.40, nome_curto(p), fonte("sans", 28, 700), INK)
    d = ImageDraw.Draw(im)
    texto_c(d, w, h - (50 if not a else 120), "BUY 1 GET 1 FREE  ·  " + MARCA, fonte("sans", 26, 700), (120, 90, 40), espaco=2)
    return im


# ======================= famílias de "conteúdo nativo" =======================

def f_email(fmt, prod, assunto, corpo):
    """AlphaGear 043 (carta/URGENT NOTICE em formato de e-mail)."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (234, 236, 240))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    m = 50
    top = 60 if not a else 220
    alto = h - top - (60 if not a else 220)
    d.rounded_rectangle((m, top, w - m, top + alto), radius=28, fill=WHITE)
    d.ellipse((m + 40, top + 40, m + 120, top + 120), fill=INK)
    texto_c_x(d, m + 80, top + 52, "P", fonte("serif", 50, 700), GOLD)
    d.text((m + 145, top + 45), MARCA.title(), font=fonte("sans", 32, 700), fill=INK)
    d.text((m + 145, top + 88), "to me", font=fonte("sans", 26, 400), fill=(120, 120, 120))
    fa = fonte("sans", 48 if not a else 54, 800)
    y = top + 160
    for l in quebrar(d, assunto, fa, w - 2 * m - 80):
        d.text((m + 40, y), l, font=fa, fill=INK)
        y += 52 if not a else 60
    fc = fonte("sans", 36 if not a else 40, 400)
    y += 16
    for par in corpo:
        for l in quebrar(d, par, fc, w - 2 * m - 80):
            d.text((m + 40, y), l, font=fc, fill=(50, 50, 55))
            y += 42 if not a else 48
        y += 14
    img_alt = top + alto - y - 140
    if img_alt > 120:
        colar_rgba(im, recorte(prod), w / 2, y + img_alt / 2, img_alt * 0.95, sombra=False)
    d = ImageDraw.Draw(im)
    pilula(d, w / 2, top + alto - 120, "CLAIM MY FREE WATCH", fonte("sans", 30, 800), INK, WHITE)
    return im


def f_carta(fmt, titulo, paragrafos, assinatura="The Pellorini team"):
    """Lucky Fours 002/038: carta só de texto em fundo claro."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (250, 247, 241))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    m = 90
    y = 90 if not a else 260
    ft = fonte("serif", 76 if not a else 84, 600)
    for l in quebrar(d, titulo, ft, w - 2 * m):
        d.text((m, y), l, font=ft, fill=INK)
        y += 78 if not a else 90
    y += 20
    fc = fonte("serif", 42 if not a else 48, 400)
    for p in paragrafos:
        for l in quebrar(d, p, fc, w - 2 * m):
            d.text((m, y), l, font=fc, fill=(45, 42, 38))
            y += 58 if not a else 68
        y += 26
    d.text((m, y + 10), assinatura, font=caveat(56 if not a else 64), fill=(90, 70, 40))
    return im


def f_tweet(fmt, prod, txt):
    """Lucky Fours 029/036: post estilo X/Twitter da própria marca."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    m = 60
    y = 70 if not a else 260
    d.ellipse((m, y, m + 96, y + 96), fill=INK)
    texto_c_x(d, m + 48, y + 14, "P", fonte("serif", 58, 700), GOLD)
    d.text((m + 120, y + 8), MARCA.title(), font=fonte("sans", 34, 800), fill=INK)
    d.ellipse((m + 120 + d.textlength(MARCA.title(), font=fonte("sans", 34, 800)) + 10, y + 16, m + 120 + d.textlength(MARCA.title(), font=fonte("sans", 34, 800)) + 40, y + 46), fill=(29, 155, 240))
    d.text((m + 120, y + 52), "@pellorini", font=fonte("sans", 28, 400), fill=(110, 118, 125))
    y += 140
    ft = fonte("sans", 44 if not a else 50, 500)
    for l in quebrar(d, txt, ft, w - 2 * m):
        d.text((m, y), l, font=ft, fill=(15, 20, 25))
        y += 58 if not a else 66
    y += 24
    alt = h - y - (90 if not a else 260)
    card = fundo(w - 2 * m, int(alt), (26, 24, 22), (4, 4, 4))
    colar_relogio(card, foto(prod), card.width / 2, card.height / 2, card.height * 0.9)
    msk = Image.new("L", card.size, 0)
    ImageDraw.Draw(msk).rounded_rectangle((0, 0, card.width, card.height), radius=30, fill=255)
    im.paste(card, (m, int(y)), msk)
    d.text((m, y + alt + 22), "9:41 AM · " + "2.4K Likes", font=fonte("sans", 26, 400), fill=(110, 118, 125))
    return im


def f_imessage(fmt, prod, falas):
    """Pascal Design 040 / Lucky Fours 033: conversa de mensagens (dramatização, sem depoimento)."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    y = 60 if not a else 220
    fb = fonte("sans", 36 if not a else 40, 500)
    for quem, txt in falas:
        if quem == "img":
            alt = 360 if not a else 600
            card = fundo(int(alt * 0.85), alt, (26, 24, 22), (4, 4, 4))
            colar_relogio(card, foto(prod), card.width / 2, card.height / 2, card.height * 0.92)
            msk = Image.new("L", card.size, 0)
            ImageDraw.Draw(msk).rounded_rectangle((0, 0, card.width, card.height), radius=36, fill=255)
            im.paste(card, (w - 60 - card.width, int(y)), msk)
            y += alt + 24
            continue
        linhas = quebrar(d, txt, fb, w * 0.62)
        bw = max(d.textlength(l, font=fb) for l in linhas) + 60
        bh = len(linhas) * (48 if not a else 54) + 34
        eu = quem == "eu"
        x0 = w - 60 - bw if eu else 60
        d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=36, fill=(10, 132, 255) if eu else (233, 233, 235))
        yy = y + 16
        for l in linhas:
            d.text((x0 + 30, yy), l, font=fb, fill=WHITE if eu else INK)
            yy += 48 if not a else 54
        y += bh + 22
    d.text((w - 220, y), "Delivered", font=fonte("sans", 26, 500), fill=(140, 140, 145))
    marca(d, w, h - (80 if not a else 200), (120, 110, 90), 28)
    return im


# ======================= famílias em fundo escuro (packshot) =======================

def f_poster(fmt, prod, linha):
    """Venezianico 009-015: pôster de lançamento, nome do modelo grande, 1 linha."""
    w, h = FORMATOS[fmt]
    c = cor_mostrador(prod)
    escura = tuple(int(v * 0.35) for v in c)
    im = fundo(w, h, escura, (4, 4, 4))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 50 if not a else 150, nome_curto(prod).upper(), fonte("serif", 120 if not a else 150, 600), CREAM, espaco=6)
    texto_c(d, w, 200 if not a else 340, linha, fonte("sans", 30 if not a else 36, 500), GOLD, espaco=2)
    colar_relogio(im, foto(prod), w / 2, 640 if not a else 1110, 640 if not a else 1050)
    d = ImageDraw.Draw(im)
    marca(d, w, h - (70 if not a else 170), (200, 192, 180), 28)
    return im


def f_limited(fmt, prod, sub):
    """Chrono Customs 017/026: 'edição limitada' com brilho da cor do mostrador."""
    w, h = FORMATOS[fmt]
    c = cor_mostrador(prod)
    im = fundo(w, h, tuple(min(255, int(v * 0.9)) for v in c), (5, 5, 5))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 50 if not a else 150, "LIMITED EDITION", fonte("anton", 110 if not a else 130), WHITE)
    texto_c(d, w, 180 if not a else 320, nome_curto(prod).upper(), fonte("sans", 34, 700), CREAM, espaco=10)
    colar_relogio(im, foto(prod), w / 2, 620 if not a else 1080, 620 if not a else 1000)
    d = ImageDraw.Draw(im)
    texto_c(d, w, h - (110 if not a else 240), sub, fonte("sans", 32 if not a else 38, 700), WHITE)
    texto_c(d, w, h - (60 if not a else 180), "ONLY A FEW MADE  ·  CLAIM YOURS", fonte("sans", 26, 600), GOLD, espaco=3)
    return im


def f_cores(fmt, prod, packs):
    """Marble Veil 001/032: foto principal + miniaturas das outras cores."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 50 if not a else 140, nome_curto(prod), fonte("serif", 90 if not a else 110, 600), CREAM)
    texto_c(d, w, 165 if not a else 290, f"AVAILABLE IN {len(packs)} FINISHES", fonte("sans", 30, 700), GOLD, espaco=4)
    colar_relogio(im, abrir(packs[0]), w / 2, 540 if not a else 900, 520 if not a else 820)
    n = len(packs) - 1
    tam = min(250, (w - 80) / max(1, n))
    y = (850 if not a else 1430)
    for i, p in enumerate(packs[1:]):
        cx = w / 2 + (i - (n - 1) / 2) * tam
        colar_relogio(im, abrir(p), cx, y + tam / 2, tam * 0.95)
    d = ImageDraw.Draw(im)
    if a:
        pilula(d, w / 2, 1700, "PICK ANY TWO · 2ND FREE", fonte("sans", 34, 800), GOLD, INK)
    return im


def f_maleta(fmt, prods, titulo="PICK 2. PAY FOR 1."):
    """Pelvini 002/030: colagem de muitos modelos 'na maleta' (feltro verde)."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (14, 54, 46))
    ruido = Image.effect_noise((w, h), 18).convert("RGB")
    im = Image.blend(im, ImageChops.multiply(im, ruido.point(lambda v: 200 + v // 5)), 0.5)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    texto_c(d, w, 40 if not a else 110, titulo, fonte("anton", 96 if not a else 120), CREAM)
    cols, rows = (4, 3) if not a else (3, 5)
    top = 180 if not a else 300
    rod = 70 if not a else 160
    cw, ch = (w - 60) / cols, (h - top - rod) / rows
    for i, p in enumerate(prods[: cols * rows]):
        x0 = 30 + cw * (i % cols)
        y0 = top + ch * (i // cols)
        slot = fundo(int(cw - 16), int(ch - 16), (30, 30, 30), (6, 6, 6))
        colar_relogio(slot, foto(p), slot.width / 2, slot.height / 2, slot.height * 0.92)
        msk = Image.new("L", slot.size, 0)
        ImageDraw.Draw(msk).rounded_rectangle((0, 0, slot.width, slot.height), radius=18, fill=255)
        im.paste(slot, (int(x0 + 8), int(y0 + 8)), msk)
    d = ImageDraw.Draw(im)
    marca(d, w, h - rod + (18 if not a else 60), GOLD, 28)
    return im


def f_sazonal(fmt, a_, b_, tema):
    """Lucky Fours (BOGO por data comemorativa) + AlphaGear 011-016 (caixa de presente sazonal)."""
    w, h = FORMATOS[fmt]
    temas = {
        "blackfriday": ((10, 10, 10), (40, 0, 0), "BLACK FRIDAY", "BUY 1 GET 1 FREE", (225, 30, 40)),
        "christmas": ((12, 50, 34), (4, 18, 12), "THE GIFT THAT LASTS", "BUY 1 GET 1 FREE THIS CHRISTMAS", GOLD),
        "valentine": ((90, 14, 34), (30, 4, 10), "ONE FOR YOU.|ONE FOR THEM.", "VALENTINE'S BOGO", (255, 160, 180)),
    }
    c1, c2, tit, sub, ac = temas[tema]
    im = fundo(w, h, c2, c1)
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    ft = fonte("anton", 110 if not a else 130)
    y = 50 if not a else 150
    for l in (tit.split("|") if "|" in tit else quebrar(d, tit, ft, w - 80)):
        texto_c(d, w, y, l, ft, ac if tema == "blackfriday" else CREAM)
        y += 125 if not a else 150
    cy = y + (300 if not a else 480)
    colar_relogio(im, foto(a_), w * 0.32, cy, 520 if not a else 780)
    colar_relogio(im, foto(b_), w * 0.68, cy, 520 if not a else 780)
    d = ImageDraw.Draw(im)
    pilula(d, w / 2, h - (130 if not a else 300), sub, fonte("sans", 32 if not a else 38, 800), ac, INK if tema != "blackfriday" else WHITE)
    texto_c(d, w, h - (50 if not a else 160), "FREE WORLDWIDE SHIPPING  ·  90-DAY RETURNS", fonte("sans", 24, 600), (220, 210, 200), espaco=2)
    return im


def f_detalhes(fmt, prod, outras):
    """Pascal Design 044/054: grade de detalhes com legendas."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), (12, 12, 12))
    d = ImageDraw.Draw(im)
    a = eh_alto(fmt)
    top = 130 if not a else 300
    texto_c(d, w, 35 if not a else 150, "The details", fonte("serif", 72 if not a else 88, 600), CREAM)
    cols, rows = 2, 2
    cw, ch = w / 2, (h - top - (20 if not a else 160)) / 2
    fontes_img = [foto(prod)] + [abrir(o) for o in outras][:3]
    rot = ["316L stainless steel", "Sapphire crystal", "Adjustable bracelet", "2-year warranty"]
    for i, ft in enumerate(fontes_img[:4]):
        x0, y0 = int(cw * (i % 2)), int(top + ch * (i // 2))
        cel = cobrir(ft, int(cw - 8), int(ch - 8))
        im.paste(cel, (x0 + 4, y0 + 4))
        d.rectangle((x0 + 4, y0 + ch - 62, x0 + cw - 4, y0 + ch - 4), fill=(0, 0, 0))
        texto_c_x(d, x0 + cw / 2, y0 + ch - 52, rot[i], fonte("sans", 28, 700), CREAM)
    return im


# ======================= famílias com foto no pulso (lifestyle) =======================

def f_split(fmt, foto_vida, prod):
    """Pascal Design 001/004: metade lifestyle, metade branca com logo, packshot e nome."""
    w, h = FORMATOS[fmt]
    a = eh_alto(fmt)
    im = Image.new("RGB", (w, h), WHITE)
    if not a:
        im.paste(cobrir(abrir(foto_vida), w // 2, h), (0, 0))
        cx, top = w * 0.75, 0
        area_h = h
    else:
        im.paste(cobrir(abrir(foto_vida), w, h // 2), (0, 0))
        cx, top = w / 2, h // 2
        area_h = h // 2
    d = ImageDraw.Draw(im)
    texto_c_x(d, cx, top + 60, MARCA, fonte("serif", 40, 600), INK, 10)
    colar_rgba(im, recorte(prod), cx, top + area_h * 0.50, area_h * 0.55)
    d = ImageDraw.Draw(im)
    texto_c_x(d, cx, top + area_h - 170, nome_curto(prod), fonte("serif", 52, 500), INK)
    texto_c_x(d, cx, top + area_h - 100, "Buy 1 Get 1 Free", fonte("sans", 30, 600), (130, 100, 50))
    return im


def f_pulso_frase(fmt, foto_vida, frase):
    """Lucky Fours 006/008: foto no pulso com frase em etiqueta estilo story."""
    w, h = FORMATOS[fmt]
    a = eh_alto(fmt)
    im = cobrir(abrir(foto_vida), w, h, 0.45)
    d = ImageDraw.Draw(im)
    fb = fonte("sans", 54 if not a else 62, 800)
    linhas = quebrar(d, frase, fb, w - 200)
    y = 90 if not a else 260
    for l in linhas:
        lw = d.textlength(l, font=fb)
        d.rounded_rectangle((w / 2 - lw / 2 - 26, y - 6, w / 2 + lw / 2 + 26, y + (74 if not a else 84)), radius=16, fill=WHITE)
        d.text((w / 2 - lw / 2, y), l, font=fb, fill=INK)
        y += 84 if not a else 94
    marca(d, w, h - (70 if not a else 200), WHITE, 28)
    return im


def f_estudio(fmt, foto_vida):
    """Aston Paris 010-016: foto limpa, sem texto além da marca."""
    w, h = FORMATOS[fmt]
    im = cobrir(abrir(foto_vida), w, h, 0.45)
    im = degrade_baixo(im, 0.78, 170)
    d = ImageDraw.Draw(im)
    marca(d, w, h - (70 if not eh_alto(fmt) else 180), WHITE, 30)
    return im


def f_vida_bogo(fmt, foto_vida):
    """Pelvini 043 / AlphaGear 010: foto no pulso + BOGO embaixo."""
    w, h = FORMATOS[fmt]
    a = eh_alto(fmt)
    im = degrade_baixo(cobrir(abrir(foto_vida), w, h, 0.4), 0.5, 240)
    d = ImageDraw.Draw(im)
    texto_c(d, w, h - (270 if not a else 470), "BUY 1 GET 1 FREE", fonte("anton", 110 if not a else 130), WHITE)
    texto_c(d, w, h - (140 if not a else 310), "FREE WORLDWIDE SHIPPING  ·  90-DAY RETURNS", fonte("sans", 26 if not a else 30, 600), GOLD, espaco=2)
    marca(d, w, h - (80 if not a else 200), WHITE, 26)
    return im


def f_postit(fmt, base, txt, base_e_produto=False):
    """Lucky Fours 009/013/023: post-it amarelo escrito à mão sobre a foto."""
    w, h = FORMATOS[fmt]
    a = eh_alto(fmt)
    if base_e_produto:
        im = fundo(w, h, (60, 58, 56), (20, 20, 20))
        colar_relogio(im, foto(base), w / 2, h * 0.58, h * (0.70 if not a else 0.55))
    else:
        im = cobrir(abrir(base), w, h, 0.45)
    lado = 400 if not a else 470
    nota = Image.new("RGBA", (lado, lado), (255, 228, 92, 255))
    dn = ImageDraw.Draw(nota)
    fm = mao(58 if len(txt) < 30 else 48)
    y = 50
    for l in txt.split("\n"):
        dn.text(((lado - dn.textlength(l, font=fm)) / 2, y), l, font=fm, fill=(25, 25, 25))
        y += 78 if len(txt) < 30 else 66
    sombra = Image.new("RGBA", (lado + 40, lado + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle((20, 26, lado + 20, lado + 26), fill=(0, 0, 0, 90))
    sombra = sombra.filter(ImageFilter.GaussianBlur(10))
    ang = random.choice([-7, -5, 4, 6])
    nota = nota.rotate(ang, expand=True, resample=Image.BICUBIC)
    sombra = sombra.rotate(ang, expand=True, resample=Image.BICUBIC)
    x, yy = (w - nota.width) // 2 + random.choice([-160, 160]), 60 if not a else 200
    im.paste(sombra, (x - 10, yy - 6), sombra)
    im.paste(nota, (x, yy), nota)
    return im


# ======================= montagem do lote =======================

def pulsos_de(lista, prefixo_excluir=()):
    return [f for f in lista if not f.startswith(prefixo_excluir)]


def packs_de(handle):
    return sorted(k for k, v in CLASS["tipos"].items() if v == "packshot" and k.startswith(handle + "_"))


def montar():
    H = CLASS["pulso_homem"]
    M = CLASS["pulso_mulher"]
    plano = []

    def add(fam, nome, fn, *args):
        plano.append((fam, nome, fn, args))

    # BOGO saturado (AlphaGear)
    pares = [("vittorio", "pelvini-clovera", (242, 107, 29)), ("pelvini-milano", "pelvini-opulent", (246, 197, 49)),
             ("titan", "pelvini-serafina", (242, 107, 29)), ("pelvini-lucent", "pelvini-dante", (246, 197, 49)),
             ("pelvini-maretti-1", "pelvini-portofina", (225, 48, 48)), ("pelvini-opulent", "pelvini-lunetta", (225, 48, 48))]
    for a_, b_, cor in pares:
        add("bogo-saturado", f"C1_P2_bogo-saturado_{nome_curto(a_)}-{nome_curto(b_)}", f_bogo_saturado, a_, b_, cor)
    # Is a name worth (Laphont) e VS designer (Monomods)
    for p in ["pelvini-milano", "pelvini-opulent", "pelvini-lucent", "titan"]:
        add("is-name-worth", f"C2_P1_is-name-worth_{nome_curto(p)}", f_is_name_worth, p)
    for p in ["vittorio", "pelvini-maretti-1", "pelvini-dante", "pelvini-portofina"]:
        add("vs-designer", f"C2_P1_vs-designer_{nome_curto(p)}", f_vs_designer, p)
    # Qual você (AlphaGear)
    for a_, b_, la, lb, t in [("vittorio", "pelvini-napoli", "CLASSIC", "ICED", "Which one are you?"),
                              ("pelvini-milano", "pelvini-lucent", "SILVER", "GOLD", "Silver or gold?"),
                              ("titan", "pelvini-opulent", "CHRONO", "CLEAN", "Which one are you?"),
                              ("pelvini-clovera", "pelvini-serafina", "DELICATE", "BOLD", "Which one is her?")]:
        add("qual-voce", f"C7_P1_qual-voce_{la.lower()}-{lb.lower()}", f_qual_voce, a_, b_, la, lb, t)
    # Ranking (AlphaGear)
    add("ranking", "C2_P1_ranking_classicos", f_ranking, ["pelvini-milano", "pelvini-opulent", "vittorio", "titan"], "4 watches that never go out of style")
    add("ranking", "C7_P5_ranking_femininos", f_ranking, ["pelvini-clovera", "pelvini-serafina", "pelvini-lunetta", "pelvini-fiorella"], "4 watches she'll wear every single day")
    # E-mail (AlphaGear 043)
    add("email", "C8_P2_email_free-watch", f_email, "pelvini-milano", "Your second watch is free (today only)",
        ["Buy any Pellorini watch and pick a second one on us.", "No code needed. It's applied in your cart."])
    add("email", "C4_P3_email-garantia", f_email, "pelvini-opulent", "Try it for 90 days. Love it or get your money back.",
        ["Every Pellorini comes with a 2-year warranty and free tracked worldwide shipping."])
    # Carta (Lucky Fours)
    add("carta", "C2_P1_carta_logo-tax", f_carta, "Why we started Pellorini",
        ["Most of what you pay for a designer watch is the name on the dial.",
         "We use the same kind of materials people expect from a luxury watch: 316L stainless steel, sapphire crystal, an adjustable bracelet.",
         "Then we skip the markup. And right now, the second watch is on us."])
    add("carta", "C4_P3_carta_90-dias", f_carta, "A watch you can return in 90 days",
        ["We know buying a watch online feels like a risk.",
         "So wear it for 90 days. Show it off. If you don't love it, send it back for a full refund.",
         "Every Pellorini is also covered by a 2-year warranty."])
    # Tweet (Lucky Fours)
    for p, t in [("pelvini-milano", "Unpopular opinion: you don't need to spend $5,000 to look like you did."),
                 ("titan", "Buy one watch. Get a second one free. That's it. That's the tweet."),
                 ("pelvini-clovera", "The best gifts are the ones they actually wear every day.")]:
        add("tweet", f"C2_P1_tweet_{nome_curto(p)}", f_tweet, p, t)
    # iMessage (Pascal/Lucky) — dramatização de presente, sem depoimento
    add("imessage", "C1_P2_imessage_aniversario", f_imessage, "pelvini-serafina",
        [("eu", "Happy anniversary. Check your bag"), ("img", ""), ("ela", "WAIT. Is this for me??"), ("eu", "The second one was free, so I got one for me too")])
    add("imessage", "C1_P2_imessage_pai", f_imessage, "titan",
        [("eu", "Dad, did the package arrive?"), ("img", ""), ("ela", "It's beautiful. You shouldn't have"), ("eu", "It was buy 1 get 1. Mine matches yours")])
    # Pôster de lançamento (Venezianico): 1 por modelo masculino
    for p in ["vittorio", "pelvini-milano", "pelvini-opulent", "pelvini-maretti-1", "titan", "pelvini-dante", "pelvini-lucent",
              "pelvini-portofina", "pelvini-dominante", "pelvini-bellagio", "pelvini-aureo", "pelvini-nocturne", "pelvini-caelus", "pelvini-forte"]:
        add("poster", f"C7_P1_poster_{nome_curto(p)}", f_poster, p, "316L STEEL  ·  BUY 1 GET 1 FREE")
    for p in ["pelvini-clovera", "pelvini-serafina", "pelvini-lunetta", "pelvini-fiorella", "pelvini-luna-perla", "pelvini-grazia"]:
        add("poster", f"C7_P5_poster_{nome_curto(p)}", f_poster, p, "EVERYDAY ELEGANCE  ·  2ND ONE FREE")
    # Edição limitada (Chrono Customs) — só os modelos marcados como Limited Edition na loja
    add("limited", "C6_P1_limited_abito", f_limited, "pelvini-abito-limited-edition-1", "EACH FINISH LIMITED TO 100 PIECES")
    add("limited", "C6_P5_limited_serpina", f_limited, "pelvini-serpina", "THE SERPINA, LIMITED EDITION")
    # Cores disponíveis (Marble Veil)
    for p in ["titan", "pelvini-opulent", "pelvini-milano", "vittorio", "pelvini-dominante", "pelvini-caelus", "pelvini-maretti-1", "pelvini-abito-limited-edition-1"]:
        pk = packs_de(p)
        if len(pk) >= 3:
            add("cores", f"C7_P1_cores_{nome_curto(p)}", f_cores, p, pk[:6])
    # Maleta (Pelvini BF)
    homens = ["vittorio", "pelvini-milano", "pelvini-opulent", "pelvini-maretti-1", "titan", "pelvini-dante", "pelvini-lucent", "pelvini-portofina",
              "pelvini-dominante", "pelvini-bellagio", "pelvini-aureo", "pelvini-caelus", "pelvini-nocturne", "pelvini-forte", "pelvini-venti"]
    mulheres = ["pelvini-clovera", "pelvini-serafina", "pelvini-lunetta", "pelvini-fiorella", "pelvini-luna-perla", "pelvini-grazia",
                "pelvini-aria", "pelvini-valentina", "pelvini-gemma", "pelvini-carina", "pelvini-perla", "pelvini-aurora", "pelvini-livia", "pelvini-bellissima", "pelvini-serpina"]
    add("maleta", "C8_P2_maleta_homem", f_maleta, homens)
    add("maleta", "C8_P5_maleta_mulher", f_maleta, mulheres)
    # Sazonais (Lucky Fours / AlphaGear)
    for tema, a_, b_ in [("blackfriday", "pelvini-milano", "pelvini-lucent"), ("blackfriday", "titan", "pelvini-serafina"),
                         ("christmas", "pelvini-opulent", "pelvini-clovera"), ("christmas", "vittorio", "pelvini-dante"),
                         ("valentine", "pelvini-maretti-1", "pelvini-luna-perla"), ("valentine", "titan", "pelvini-fiorella")]:
        add("sazonal", f"C8_P2_sazonal-{tema}_{nome_curto(a_)}-{nome_curto(b_)}", f_sazonal, a_, b_, tema)
    # Detalhes (Pascal)
    for p in ["vittorio", "pelvini-milano", "titan", "pelvini-opulent"]:
        outras = [k for k in CLASS["estudio"] + CLASS["pulso"] if k.startswith(p + "_")]
        if len(outras) >= 1:
            add("detalhes", f"C3_P3_detalhes_{nome_curto(p)}", f_detalhes, p, (outras * 3)[:3])
    # Lifestyle
    prod_de = lambda f: f.rsplit("_", 1)[0]
    vida_h = H[:12]
    vida_m = M[:16]
    frases_h = ["The watch people ask about.", "Looks expensive. Isn't.", "Your new everyday watch.", "Dressed up or down. Always on.",
                "Built from 316L steel. Made to be worn.", "The look of a $10K watch."]
    frases_m = ["Small details. Big difference.", "The everyday piece she'll never take off.", "Gold that goes with everything.",
                "Delicate, not fragile.", "A gift she'll wear every day.", "Quiet luxury, every day."]
    for i, f in enumerate(vida_h):
        add("split", f"C7_P1_split_{f[:-4]}", f_split, f, prod_de(f))
        add("pulso-frase", f"C2_P1_pulso-frase_{f[:-4]}", f_pulso_frase, f, frases_h[i % len(frases_h)])
        add("estudio", f"C7_P1_estudio_{f[:-4]}", f_estudio, f)
        add("vida-bogo", f"C1_P2_vida-bogo_{f[:-4]}", f_vida_bogo, f)
    for i, f in enumerate(vida_m):
        if i % 2 == 0:
            add("split", f"C7_P5_split_{f[:-4]}", f_split, f, prod_de(f))
        add("pulso-frase", f"C7_P5_pulso-frase_{f[:-4]}", f_pulso_frase, f, frases_m[i % len(frases_m)])
        add("estudio", f"C7_P5_estudio_{f[:-4]}", f_estudio, f)
        if i % 2 == 1:
            add("vida-bogo", f"C1_P2_vida-bogo_{f[:-4]}", f_vida_bogo, f)
    # Post-it (Lucky Fours)
    notas = ["2nd watch\nFREE\nends tonight", "BUY 1\nGET 1\nFREE", "no code\nneeded :)", "looks like\n$10K\n(it's not)", "90 days\nto love it\nor return it", "one for you\none for them"]
    bases = vida_h[:4] + vida_m[:4]
    for i, b in enumerate(bases):
        add("postit", f"C8_P2_postit_{b[:-4]}", f_postit, b, notas[i % len(notas)])
    for i, p in enumerate(["pelvini-milano", "titan", "pelvini-opulent", "vittorio"]):
        add("postit", f"C8_P2_postit-produto_{nome_curto(p)}", f_postit, p, notas[(i + 2) % len(notas)], True)
    return plano


def folha(arquivos, saida, w=300, cols=8):
    ims = []
    for f in arquivos:
        im = Image.open(f)
        im.thumbnail((w, int(w * 16 / 9)))
        ims.append((f, im))
    hcel = max(i.height for _, i in ims) + 20
    rows = (len(ims) + cols - 1) // cols
    fo = Image.new("RGB", (cols * w, rows * hcel), "white")
    d = ImageDraw.Draw(fo)
    for k, (f, im) in enumerate(ims):
        x, y = (k % cols) * w, (k // cols) * hcel
        fo.paste(im, (x, y))
        d.text((x + 2, y + im.height + 3), os.path.basename(f)[:44], fill="black")
    fo.save(saida, quality=80)


if __name__ == "__main__":
    import sys
    so = sys.argv[1:]  # opcional: só algumas famílias
    plano = montar()
    feitos, erros = [], []
    for fam, nome, fn, args in plano:
        if so and fam not in so:
            continue
        os.makedirs(os.path.join(SAIDA, fam), exist_ok=True)
        for fmt in FORMATOS:
            out = os.path.join(SAIDA, fam, f"{nome}_{fmt}.jpg")
            try:
                fn(fmt, *args).convert("RGB").save(out, quality=92)
                feitos.append(out)
            except Exception as e:
                erros.append(f"{nome} {fmt}: {e.__class__.__name__}: {e}")
    print(len(feitos), "imagens |", len(erros), "erros")
    for e in erros[:30]:
        print("  ", e)
    q = sorted(f for f in feitos if f.endswith("_1x1.jpg"))
    for i in range(0, len(q), 48):
        folha(q[i:i + 48], os.path.join(SAIDA, f"_revisao_1x1_{i // 48 + 1:02d}.jpg"))
    v = sorted(f for f in feitos if f.endswith("_9x16.jpg"))
    for i in range(0, len(v), 40):
        folha(v[i:i + 40], os.path.join(SAIDA, f"_revisao_9x16_{i // 40 + 1:02d}.jpg"), w=220, cols=10)

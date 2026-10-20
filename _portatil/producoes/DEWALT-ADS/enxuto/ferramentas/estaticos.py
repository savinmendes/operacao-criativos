# -*- coding: utf-8 -*-
"""Monta os estaticos C5 (foto IA + texto local) e C6 (recortes reais do banco)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

BASE = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\enxuto")
T = BASE / "trabalho"; C6 = T / "c6"; OUT = BASE / "pecas"
FD = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
ANTON = str(FD / "Anton-Regular.ttf"); POP = str(FD / "Poppins-Bold.ttf")
AMA = (254, 189, 17); PRETO = (18, 18, 18); BRANCO = (255, 255, 255)


def F(p, s):
    return ImageFont.truetype(p, s)


def trim(im):
    a = np.array(im.split()[-1]); a[a < 25] = 0
    im.putalpha(Image.fromarray(a)); return im.crop(im.getbbox())


def solid(im, lim=60):
    a = np.array(im.split()[-1]).astype(np.float32)
    a = np.clip((a - 20) * 255 / lim, 0, 255).astype(np.uint8)
    im.putalpha(Image.fromarray(a)); return im


def cut(nome, apagar=None, reforcar=False):
    im = Image.open(C6 / nome).convert("RGBA")
    if apagar:
        a = np.array(im); x0, y0, x1, y1 = apagar; a[y0:y1, x0:x1, 3] = 0; im = Image.fromarray(a)
    if reforcar:
        im = solid(im)
    return trim(im)


def fit(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)


def sombra(canvas, im, x, y, blur=18, off=14, alpha=150):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); a = im.split()[-1].point(lambda v: alpha if v > 30 else 0)
    sh.putalpha(a); pad = blur * 3
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.paste(sh, (pad, pad), sh)
    big = big.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(big, (max(0, x - pad + off // 2), max(0, y - pad + off)))
    canvas.alpha_composite(im, (x, y))


def texto_c(d, cx, y, txt, fonte, cor, contorno=0, cor_c=PRETO):
    w = d.textlength(txt, font=fonte)
    d.text((cx - w / 2, y), txt, font=fonte, fill=cor, stroke_width=contorno, stroke_fill=cor_c)


def pill(d, cx, y, txt, fonte, fundo, cor, padx=28, pady=12):
    l, t, r, b = d.textbbox((0, 0), txt, font=fonte); w = r - l; h = b - t
    d.rounded_rectangle((cx - w / 2 - padx, y, cx + w / 2 + padx, y + h + 2 * pady), radius=(h + 2 * pady) // 2, fill=fundo)
    d.text((cx - w / 2 - l, y + pady - t), txt, font=fonte, fill=cor)
    return y + h + 2 * pady


def fundo(W, H):
    yy = np.linspace(0, 1, H)[:, None, None]
    g = np.array([38, 38, 40]) * (1 - yy) + np.array([12, 12, 13]) * yy
    g = np.broadcast_to(g, (H, W, 3)).astype(np.uint8)
    im = Image.fromarray(g).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(-H, W, 46):
        d.line((i, 0, i + H, H), fill=(255, 255, 255, 7), width=2)
    im.alpha_composite(lay)
    return im


def item_label(d, cx, y, l1, l2, s1, s2):
    texto_c(d, cx, y, l1, F(ANTON, s1), AMA)
    texto_c(d, cx, y + int(s1 * 1.32), l2, F(POP, s2), BRANCO)


def c6(W, H):
    im = fundo(W, H); d = ImageDraw.Draw(im); k = W / 1080; alto = H / W > 1.5
    tal = cut("taladro_02_cut.png"); mal = cut("maleta_u2net.png")
    bat1 = cut("bat_b_i.png"); bat2 = cut("bat_a_i.png", apagar=(430, 0, 500, 80), reforcar=True)
    car = cut("carr_i.png", reforcar=True)
    y = int(60 * k if alto else 34 * k)
    y = pill(d, W / 2, y, "PRE BLACK FRIDAY", F(POP, int(34 * k)), AMA, PRETO) + int(22 * k)
    texto_c(d, W / 2, y, "QUÉ INCLUYE TU KIT", F(ANTON, int((118 if alto else 100) * k)), BRANCO)
    y += int((165 if alto else 138) * k)
    texto_c(d, W / 2, y, "Kit Taladro Percutor 20V MAX", F(POP, int(40 * k)), AMA); y += int(70 * k)
    zona = (y + int(20 * k), H - int(300 * k)) if alto else (y + int(6 * k), H - int(170 * k))
    zh = zona[1] - zona[0]; fs1, fs2 = int((50 if alto else 40) * k), int((28 if alto else 24) * k)
    lab = int(fs1 * 1.32 + fs2 * 1.5)
    colw = W // 2
    # linha 1: taladro + maletin
    h1 = int(zh * 0.56) - lab
    t = fit(tal, colw - int(40 * k), h1); m = fit(mal, colw - int(80 * k), int(h1 * 0.80))
    sombra(im, t, colw // 2 - t.width // 2 + int(20 * k), zona[0] + h1 - t.height)
    sombra(im, m, colw + colw // 2 - m.width // 2 - int(10 * k), zona[0] + h1 - m.height)
    d = ImageDraw.Draw(im)
    item_label(d, colw // 2 + int(20 * k), zona[0] + h1 + int(12 * k), "TALADRO PERCUTOR", "y atornillador · 20V MAX brushless", fs1, fs2)
    item_label(d, colw + colw // 2, zona[0] + h1 + int(12 * k), "MALETÍN", "para guardar y llevar todo", fs1, fs2)
    # linha 2: 2 baterias + cargador
    y2 = zona[0] + int(zh * 0.56) + int(18 * k); h2 = zona[1] - y2 - lab
    b1 = fit(bat1, int(colw * 0.62), int(h2 * 0.62)); b2 = fit(bat2, int(colw * 0.62), int(h2 * 0.62))
    bx = colw // 2
    sombra(im, b2, bx - b2.width // 2 + int(70 * k), y2 + h2 - b2.height - int(h2 * 0.30))
    sombra(im, b1, bx - b1.width // 2 - int(50 * k), y2 + h2 - b1.height)
    c = fit(car, colw - int(110 * k), int(h2 * 0.88))
    sombra(im, c, colw + colw // 2 - c.width // 2, y2 + h2 - c.height)
    d = ImageDraw.Draw(im)
    d.text((bx + int(150 * k), y2 + int(4 * k)), "x2", font=F(ANTON, int(64 * k)), fill=AMA)
    item_label(d, bx, y2 + h2 + int(12 * k), "2 BATERÍAS 2Ah", "una trabaja, otra cargando", fs1, fs2)
    item_label(d, colw + colw // 2, y2 + h2 + int(12 * k), "CARGADOR", "carga tus baterías 20V", fs1, fs2)
    bh = int((210 if alto else 130) * k); d.rectangle((0, H - bh, W, H), fill=AMA)
    if alto:
        texto_c(d, W / 2, H - bh + int(34 * k), "PAGAS CUANDO LO RECIBES", F(ANTON, int(76 * k)), PRETO)
        texto_c(d, W / 2, H - bh + int(138 * k), "Envío a todo Chile", F(POP, int(36 * k)), PRETO)
    else:
        texto_c(d, W / 2, H - bh + int(18 * k), "PAGAS CUANDO LO RECIBES", F(ANTON, int(60 * k)), PRETO)
        texto_c(d, W / 2, H - bh + int(88 * k), "Envío a todo Chile", F(POP, int(26 * k)), PRETO)
    return im.convert("RGB")


def c5(W, H):
    src = Image.open(T / "img_c5.png").convert("RGB")
    r = W / src.width; src = src.resize((W, int(src.height * r)), Image.LANCZOS)
    if src.height > H:
        top = int(src.height * 0.50) - H // 2 if H / W > 1.5 else int(200 * W / 1080)
        top = max(0, min(src.height - H, top))
        src = src.crop((0, top, W, top + H))
    im = src.convert("RGBA"); k = W / 1080; alto = H / W > 1.5
    px = []
    for yy in range(H):
        t = yy / H; a = 0
        if t < (0.30 if H / W > 1.5 else 0.26):
            a = int(215 * (1 - t / (0.30 if H / W > 1.5 else 0.26)) ** 1.2)
        if t > 0.66:
            a = int(235 * ((t - 0.66) / 0.34) ** 1.1)
        px.append(a)
    g = Image.new("L", (1, H)); g.putdata(px); g = g.resize((W, H))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 255)); sh.putalpha(g); im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    y = int((90 if alto else 46) * k)
    y = pill(d, W / 2, y, "PRE BLACK FRIDAY", F(POP, int(38 * k)), AMA, PRETO) + int(26 * k)
    if alto:
        texto_c(d, W / 2, y, "PAGAS CUANDO", F(ANTON, int(118 * k)), BRANCO, int(3 * k)); y += int(150 * k)
        texto_c(d, W / 2, y, "LO RECIBES", F(ANTON, int(118 * k)), AMA, int(3 * k))
    else:
        f = F(ANTON, int(86 * k)); w1 = d.textlength("PAGAS CUANDO ", font=f); w2 = d.textlength("LO RECIBES", font=f)
        x0 = (W - w1 - w2) / 2
        d.text((x0, y), "PAGAS CUANDO ", font=f, fill=BRANCO, stroke_width=int(3 * k), stroke_fill=PRETO)
        d.text((x0 + w1, y), "LO RECIBES", font=f, fill=AMA, stroke_width=int(3 * k), stroke_fill=PRETO)
    yb = H - int((330 if alto else 236) * k)
    texto_c(d, W / 2, yb, "Kit Taladro Percutor 20V MAX", F(ANTON, int(70 * k)), BRANCO, int(2 * k)); yb += int(98 * k)
    texto_c(d, W / 2, yb, "2 baterías + cargador + maletín", F(POP, int(42 * k)), AMA); yb += int(78 * k)
    pill(d, W / 2, yb, "ENVÍO A TODO CHILE", F(POP, int(32 * k)), BRANCO, PRETO)
    return im.convert("RGB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for (W, H), suf in [((1080, 1920), "9x16"), ((1080, 1350), "4x5")]:
        c6(W, H).save(OUT / f"EST_C6_incluye_{suf}.png")
        c5(W, H).save(OUT / f"EST_C5_pagas-al-recibir_{suf}.png")
    print("ok")

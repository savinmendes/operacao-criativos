# -*- coding: utf-8 -*-
"""Overlays DeWalt-like (preto + amarelo #FEBD17, SEM logo DeWalt) do kit DCD7781, 720x1280. Local (PIL), sem custo.
Saidas em edicao/ov/: banner_topo.png, selo_bf.png, tit_g1..g5.png (titulo do gancho, tela cheia),
tt_<slug>.png (titulo de frase, tela cheia), cobre37_<mat>.png (faixa verde sobre os numeros do AD 37),
cta_final.png (cartao final), sticker_kit.png, preview_overlays.jpg"""
import re
import unicodedata
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ED = Path(__file__).resolve().parent
OUT = ED / "ov"
TR = ED / "_trabalho"
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
PB, PS, AN = (str(KIT / f) for f in ("Poppins-Bold.ttf", "Poppins-SemiBold.ttf", "Anton-Regular.ttf"))
F = lambda p, s: ImageFont.truetype(p, s)
PRETO = (16, 16, 16, 255)
AMA = (254, 189, 23, 255)
BRANCO = (255, 255, 255, 255)
VERDE37 = (0, 65, 32, 255)
SS = 3
W, H = 720, 1280


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40]


def centro(d, t, f, y, cor, cx, **kw):
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, y), t, font=f, fill=cor, **kw)


def listras(w, h, a=AMA, b=PRETO, passo=22):
    """faixa de listras diagonais (estilo canteiro de obra)"""
    im = Image.new("RGBA", (w * SS, h * SS), a)
    d = ImageDraw.Draw(im)
    p = passo * SS
    for x in range(-h * SS, w * SS + h * SS, 2 * p):
        d.polygon([(x, h * SS), (x + p, h * SS), (x + p + h * SS, 0), (x + h * SS, 0)], fill=b)
    return im.resize((w, h), Image.LANCZOS)


def caixa_texto(linhas, px, cor_txt=AMA, cor_fundo=PRETO, padx=24, pady=12, angulo=0, borda=None, fonte=AN,
                larg_max=680):
    """caixa com 1+ linhas centralizadas"""
    f = F(fonte, px * SS)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbs = [tmp.textbbox((0, 0), t, font=f) for t in linhas]
    lh = max(b[3] - b[1] for b in bbs)
    gap = int(px * 0.18 * SS)
    w = max(b[2] - b[0] for b in bbs) + 2 * padx * SS
    h = lh * len(linhas) + gap * (len(linhas) - 1) + 2 * pady * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), fill=cor_fundo)
    if borda:
        d.rectangle((0, 0, w - 1, h - 1), outline=borda, width=4 * SS)
    y = pady * SS
    for t, b in zip(linhas, bbs):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], y - b[1]), t, font=f, fill=cor_txt)
        y += lh + gap
    if angulo:
        im = im.rotate(angulo, resample=Image.BICUBIC, expand=True)
    im = im.resize((im.width // SS, im.height // SS), Image.LANCZOS)
    if im.width > larg_max:
        im = im.resize((larg_max, int(im.height * larg_max / im.width)), Image.LANCZOS)
    return im


def sombra(im, r=10, off=(0, 6), alpha=150):
    pad = 3 * r
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, alpha))
    sh.putalpha(im.split()[3].point(lambda v: v * alpha // 255))
    base.alpha_composite(sh, (pad + off[0], pad + off[1]))
    base = base.filter(ImageFilter.GaussianBlur(r))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def banner():
    w, h = 470, 92
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), 14 * SS, fill=PRETO, outline=AMA, width=3 * SS)
    im = im.resize((w, h), Image.LANCZOS)
    # bloco de listras a esquerda (dentro da borda)
    st = listras(70, h - 12, passo=10)
    m = Image.new("L", st.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, st.width - 1, st.height - 1), 10, fill=255)
    im.paste(st, (6, 6), m)
    d = ImageDraw.Draw(im)
    d.text((92, 12), "PAGO CONTRA ENTREGA", font=F(PB, 27), fill=BRANCO)
    d.text((92, 47), "ENVÍO A TODO CHILE", font=F(PB, 27), fill=AMA)
    im.save(OUT / "banner_topo.png")
    return im


def selo():
    s = 176
    S = s * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=PRETO)
    d.ellipse((6 * SS, 6 * SS, S - 6 * SS, S - 6 * SS), fill=AMA)
    d.ellipse((13 * SS, 13 * SS, S - 13 * SS, S - 13 * SS), outline=PRETO, width=2 * SS)
    centro(d, "PRE", F(PB, 24 * SS), 26 * SS, PRETO, S / 2)
    centro(d, "BLACK", F(AN, 40 * SS), 54 * SS, PRETO, S / 2)
    centro(d, "FRIDAY", F(AN, 40 * SS), 98 * SS, PRETO, S / 2)
    im = im.resize((s, s), Image.LANCZOS).rotate(-8, resample=Image.BICUBIC)
    im.save(OUT / "selo_bf.png")
    return im


def titulo_gancho(nome, linhas, sub=None, y=150, px=104):
    """titulo grande do gancho (fica na parte de cima; a legenda da fala continua visivel embaixo)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx = caixa_texto(linhas, px, AMA, PRETO, padx=26, pady=14, angulo=3, borda=AMA)
    c, pad = sombra(cx)
    im.alpha_composite(c, ((W - c.width) // 2, y - pad))
    yb = y + cx.height - 6
    if sub:
        sb = caixa_texto([sub], 40, PRETO, AMA, padx=18, pady=6, angulo=3)
        c2, pad2 = sombra(sb, r=6, off=(0, 4))
        im.alpha_composite(c2, ((W - c2.width) // 2, yb - pad2))
        yb += sb.height
    im.save(OUT / f"tit_{nome}.png")
    print(f"tit_{nome}: y {y} -> {yb}")
    return im


def titulo_frase(texto, rodape=None, y=212):
    """titulo de frase: caixa preta, texto amarelo, logo abaixo do banner/selo"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    linhas = [texto]
    if len(texto) > 22 and "·" in texto:
        linhas = [p.strip() for p in texto.split("·")]
    elif len(texto) > 24 and " + " in texto:
        a, b = texto.split(" + ", 1)
        linhas = [a, "+ " + b]
    cx = caixa_texto(linhas, 54, AMA, PRETO, padx=20, pady=8, borda=AMA)
    c, pad = sombra(cx, r=8, off=(0, 4))
    im.alpha_composite(c, ((W - c.width) // 2, y - pad))
    if rodape:
        d = ImageDraw.Draw(im)
        f = F(PS, 22)
        tw = d.textlength(rodape, font=f)
        d.rounded_rectangle(((W - tw) / 2 - 12, 1196, (W + tw) / 2 + 12, 1232), 8, fill=(0, 0, 0, 170))
        centro(d, rodape, f, 1199, BRANCO, W / 2)
    nome = f"tt_{slug(texto)}.png"
    im.save(OUT / nome)
    return nome


def cobre37(mat, texto):
    """faixa verde opaca sobre o numero (38mm/13mm) e a sombra do titulo antigo, com o titulo ES"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 646, W, 866), fill=VERDE37)
    f = F(AN, 78 if len(texto) < 10 else 62)
    centro(d, texto, f, 768, AMA, W / 2)
    im.save(OUT / f"cobre37_{mat}.png")
    return im


def recorte_taladro():
    rc = Image.open(TR / "c4_cut.png").convert("RGBA")
    a = rc.split()[3].point(lambda v: 0 if v < 30 else (255 if v > 220 else v))
    rc.putalpha(a)
    return rc.crop(rc.getbbox())


def cta_final():
    im = Image.new("RGBA", (W, H), PRETO)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((90, 330, 630, 900), fill=(254, 189, 23, 120))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(110)))
    im.alpha_composite(listras(W, 34, passo=16), (0, 0))
    im.alpha_composite(listras(W, 34, passo=16), (0, H - 34))
    d = ImageDraw.Draw(im)
    centro(d, "PRE BLACK FRIDAY", F(AN, 96), 70, AMA, W / 2)
    centro(d, "Kit Taladro Percutor 20V MAX", F(PB, 38), 214, BRANCO, W / 2)
    rc = recorte_taladro()
    ph = 560
    rc = rc.resize((int(rc.width * ph / rc.height), ph), Image.LANCZOS)
    c, pad = sombra(rc, r=18, off=(0, 14), alpha=200)
    im.alpha_composite(c, ((W - rc.width) // 2 - pad, 290 - pad))
    y = 290 + ph + 30
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, y, W - 60, y + 104), 26, fill=AMA)
    centro(d, "PAGAS AL RECIBIR", F(AN, 74), y + 8, PRETO, W / 2)
    centro(d, "Envío a todo Chile", F(PB, 44), y + 128, BRANCO, W / 2)
    print("cta: termina em y", y + 128 + 56)
    im.convert("RGB").save(OUT / "cta_final.png")
    return im


def sticker():
    rc = recorte_taladro()
    h = 250
    rc = rc.resize((int(rc.width * h / rc.height), h), Image.LANCZOS)
    tag = caixa_texto(["PAGAS AL RECIBIR"], 30, PRETO, AMA, padx=12, pady=4, angulo=6)
    w = rc.width + tag.width - 30
    im = Image.new("RGBA", (w, h + 10), (0, 0, 0, 0))
    c, pad = sombra(rc, r=8, off=(0, 6), alpha=170)
    im.alpha_composite(c.crop((pad, pad, pad + rc.width, pad + rc.height)), (0, 0))
    im.alpha_composite(tag, (rc.width - 30, h - tag.height - 40))
    im = im.crop(im.getbbox())
    im.save(OUT / "sticker_kit.png")
    return im


TIT_GANCHOS = {
    "g1": (["LAS 3B"], "BUENO · BONITO · BARATO", 140),
    "g2": (["¿TU TALADRO", "NO DA MÁS?"], None, 92),
    "g3": (["PARA PEGA", "PESADA"], None, 104),
    "g4": (["PRE BLACK FRIDAY"], "DEWALT 20V MAX", 92),
    "g5": (["KIT COMPLETO"], "2 BATERÍAS + CARGADOR + MALETA", 100),
}

TIT_FRASE = [
    "TALADRO PERCUTOR Y ATORNILLADOR", "2 BATERÍAS 2Ah + CARGADOR + MALETA", 'MANDRIL 1/2" · 13 mm', "COMPACTO Y LIVIANO",
    "MOTOR SIN CARBONES", "2 VELOCIDADES", "HASTA 1.750 RPM", "15 POSICIONES DE TORQUE", "INDICADOR DE CARGA",
    "LUZ LED", "PRE BLACK FRIDAY", "TALADRO PERCUTOR Y ATORNILLADOR DEWALT", "2 BATERÍAS 20V MAX + CARGADOR", "+ MALETA",
    "INDICADOR DE CARGA + LUZ LED", "DEWALT 20V MAX", "BATERÍA 2Ah", "BRUSHLESS", "PAGAS AL RECIBIR",
    "PRE BLACK FRIDAY · PAGAS AL RECIBIR",
]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ban, sel = banner(), selo()
    tits = {k: titulo_gancho(k, *v[:2], px=v[2]) for k, v in TIT_GANCHOS.items()}
    nomes = [titulo_frase(t) for t in TIT_FRASE]
    nomes.append(titulo_frase("17% MÁS EFICIENTE*", rodape="*vs. motor con carbones, según DeWalt"))
    for m, t in (("madera", "MADERA"), ("metal", "METAL"), ("muro", "MURO Y CONCRETO")):
        cobre37(m, t)
    cta, stk = cta_final(), sticker()
    # preview: 3 quadros reais com os overlays
    q1 = Image.open(TR / "c1.png").convert("RGBA").resize((W, H))
    a = q1.copy(); a.alpha_composite(tits["g4"])
    b = Image.open(TR / "c4.png").convert("RGBA").resize((W, H))
    b.alpha_composite(ban, (16, 16)); b.alpha_composite(sel, (W - sel.width - 10, 10))
    b.alpha_composite(Image.open(OUT / "tt_17-mas-eficiente.png"))
    b.alpha_composite(stk, ((W - stk.width) // 2, H - stk.height - 40))
    c37 = Image.open(TR / "f37_band.png")  # so referencia
    sheet = Image.new("RGB", (3 * W + 40, H), (40, 40, 40))
    sheet.paste(a.convert("RGB"), (0, 0)); sheet.paste(b.convert("RGB"), (W + 20, 0)); sheet.paste(cta.convert("RGB"), (2 * W + 40, 0))
    sheet.save(OUT / "preview_overlays.jpg", quality=88)
    print("frases:", nomes)

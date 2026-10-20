# -*- coding: utf-8 -*-
"""Lote 1 de estáticos Pellorini (abordagem A: templates em código sobre as fotos da loja, custo zero).

Uso: python gerar_lote.py            -> gera lote1/*.jpg em 1:1 (1080x1080) e 9:16 (1080x1920)
Cada função de template = 1 família visual; o nome do arquivo carrega conceito_persona_angulo_execucao_formato.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(BASE, "fotos-loja")
SAIDA = os.path.join(BASE, "lote1")
F = os.path.join(BASE, "fontes")
os.makedirs(SAIDA, exist_ok=True)

GOLD = (212, 175, 106)
CREAM = (246, 240, 230)
INK = (14, 13, 12)
RED = (196, 52, 46)
GREEN = (46, 160, 90)
MARCA = "PELLORINI"
FORMATOS = {"1x1": (1080, 1080), "9x16": (1080, 1920)}


def fonte(nome, tam, peso=None):
    arq = {"serif": "PlayfairDisplay.ttf", "cond": "Oswald.ttf", "sans": "Inter.ttf", "anton": "Anton-Regular.ttf.ttf"}[nome]
    f = ImageFont.truetype(os.path.join(F, arq), tam)
    if peso:
        try:
            eixos = f.get_variation_axes()
            f.set_variation_by_axes([peso] + [a["default"] for a in eixos[1:]] if len(eixos) > 1 else [peso])
        except Exception:
            pass
    return f


def foto(handle, n=1):
    return Image.open(os.path.join(FOTOS, f"{handle}_{n}.jpg")).convert("RGB")


def fundo(w, h, c1=(26, 24, 22), c2=(4, 4, 4)):
    """Degradê radial escuro (combina com as fotos em fundo preto)."""
    g = Image.radial_gradient("L").resize((w, h))
    a = Image.new("RGB", (w, h), c1)
    b = Image.new("RGB", (w, h), c2)
    return Image.composite(b, a, g)


def colar_relogio(dest, im, cx, cy, alt, brilho=1.0):
    """Cola a foto (fundo preto) com 'lighten': o preto some sobre fundo escuro, sem recorte."""
    im = im.copy()
    r = alt / im.height
    im = im.resize((int(im.width * r), int(alt)), Image.LANCZOS)
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    reg = dest.crop((x, y, x + im.width, y + im.height))
    dest.paste(ImageChops.lighter(reg, im), (x, y))


def texto_c(d, w, y, txt, f, cor, espaco=0):
    if espaco:
        larg = sum(d.textlength(c, font=f) for c in txt) + espaco * (len(txt) - 1)
        x = (w - larg) / 2
        for c in txt:
            d.text((x, y), c, font=f, fill=cor)
            x += d.textlength(c, font=f) + espaco
        return
    larg = d.textlength(txt, font=f)
    d.text(((w - larg) / 2, y), txt, font=f, fill=cor)


def pilula(d, cx, y, txt, f, bg, fg, padx=46, pady=20):
    larg = d.textlength(txt, font=f)
    a = f.getbbox(txt)[3]
    d.rounded_rectangle((cx - larg / 2 - padx, y, cx + larg / 2 + padx, y + a + pady * 2), radius=(a + pady * 2) / 2, fill=bg)
    d.text((cx - larg / 2, y + pady - 2), txt, font=f, fill=fg)


def marca(d, w, y, cor=GOLD, tam=34):
    texto_c(d, w, y, MARCA, fonte("sans", tam, 500), cor, espaco=int(tam * 0.55))


# ---------- famílias ----------

def t_bogo_caixa(fmt, a, b, sub="ONE FOR YOU. ONE FOR THEM."):
    """C1/C8: BOGO gritado com 2 relógios lado a lado (Pelvini 010/011, AlphaGear 001)."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h)
    d = ImageDraw.Draw(im)
    v = h / 1080
    marca(d, w, 60 * v)
    alt = 560 if fmt == "1x1" else 820
    cy = 430 if fmt == "1x1" else 820
    colar_relogio(im, foto(a), w * 0.30, cy, alt)
    colar_relogio(im, foto(b), w * 0.70, cy, alt)
    d = ImageDraw.Draw(im)
    yt = 735 if fmt == "1x1" else 1330
    texto_c(d, w, yt, "BUY 1 GET 1 FREE", fonte("anton", 118 if fmt == "1x1" else 132), CREAM)
    texto_c(d, w, yt + (150 if fmt == "1x1" else 175), sub, fonte("sans", 30, 600), GOLD, espaco=3)
    pilula(d, w / 2, yt + (210 if fmt == "1x1" else 260), "SHOP NOW", fonte("sans", 30, 700), GOLD, INK)
    return im


def t_his_hers(fmt, homem, mulher):
    """C1: presente de casal (Pelvini 013/026 'One for you, one for them')."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h, (34, 28, 24), (8, 6, 5))
    d = ImageDraw.Draw(im)
    v = 1 if fmt == "1x1" else 1.6
    marca(d, w, 60 * v)
    texto_c(d, w, 120 * v, "His & Hers", fonte("serif", 96 if fmt == "1x1" else 120, 600), CREAM)
    cy = 600 if fmt == "1x1" else 1000
    colar_relogio(im, foto(homem), w * 0.33, cy, 600 if fmt == "1x1" else 860)
    colar_relogio(im, foto(mulher), w * 0.70, cy + 20, 560 if fmt == "1x1" else 800)
    d = ImageDraw.Draw(im)
    yb = 930 if fmt == "1x1" else 1560
    texto_c(d, w, yb, "Buy one, the second is on us.", fonte("serif", 44, 500), GOLD)
    if fmt == "9x16":
        pilula(d, w / 2, yb + 110, "BUY 1 GET 1 FREE", fonte("sans", 34, 700), GOLD, INK)
    return im


def icone(d, x, y, tam, bom):
    """Desenha ✓/✕ como forma (as fontes não têm o glifo ✕)."""
    if bom:
        d.ellipse((x, y, x + tam, y + tam), fill=GREEN)
        d.line((x + tam * .27, y + tam * .52, x + tam * .44, y + tam * .70, x + tam * .75, y + tam * .32), fill="white", width=max(3, tam // 9))
    else:
        d.ellipse((x, y, x + tam, y + tam), fill=RED)
        m = tam * .3
        d.line((x + m, y + m, x + tam - m, y + tam - m), fill="white", width=max(3, tam // 9))
        d.line((x + tam - m, y + m, x + m, y + tam - m), fill="white", width=max(3, tam // 9))


def t_genericoxnos(fmt, prod):
    """C3: coluna Genérico ✕ × Pellorini ✓ (Monomods 004, AlphaGear 040)."""
    w, h = FORMATOS[fmt]
    im = Image.new("RGB", (w, h), CREAM)
    d = ImageDraw.Draw(im)
    alto = fmt == "9x16"
    texto_c(d, w, 50 if not alto else 90, "Why it doesn't feel cheap", fonte("serif", 66 if not alto else 76, 600), INK)
    topo = 165 if not alto else 250
    meio = w / 2
    d.rounded_rectangle((meio - 10, topo - 25, w - 40, h - 40), radius=22, fill=INK)
    fh = fonte("sans", 30, 700)
    d.text((50, topo), "Cheap watch", font=fh, fill=(120, 112, 104))
    d.text((meio + 30, topo), MARCA, font=fh, fill=GOLD)
    linhas = [("Alloy that tarnishes", "316L stainless steel"),
              ("Glass that scratches", "Sapphire crystal"),
              ("One-size bracelet", "Adjustable + tool"),
              ("No real warranty", "2-year warranty"),
              ("Final sale", "90-day money back")]
    passo = 78 if not alto else 100
    y = topo + (70 if not alto else 95)
    fx = fonte("sans", 31 if not alto else 34, 500)
    for ruim, bom in linhas:
        icone(d, 50, y + 2, 34, False)
        d.text((98, y), ruim, font=fx, fill=(80, 74, 68))
        icone(d, meio + 30, y + 2, 34, True)
        d.text((meio + 78, y), bom, font=fx, fill=CREAM)
        y += passo
    alt = h - y - (60 if not alto else 90)
    colar_relogio(im, foto(prod), (meio + w - 40) / 2, y + alt / 2 + 10, alt * 0.95)
    d = ImageDraw.Draw(im)
    if alto:
        texto_c(d, meio, h - 260, "Same look.", fonte("serif", 60, 600), INK)
        texto_c(d, meio, h - 185, "Built to last.", fonte("serif", 60, 600), INK)
    return im


def t_garantia(fmt, prod):
    """C4: remoção de risco como ângulo principal (Lucky Fours 002 'carta', estúdio escuro)."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h)
    d = ImageDraw.Draw(im)
    v = 1 if fmt == "1x1" else 1.6
    marca(d, w, 56 * v)
    texto_c(d, w, 120 * v, "Wear it for 90 days.", fonte("serif", 78 if fmt == "1x1" else 92, 600), CREAM)
    texto_c(d, w, 215 * v, "Don't love it? Full refund.", fonte("serif", 52 if fmt == "1x1" else 62, 400), GOLD)
    colar_relogio(im, foto(prod), w / 2, 640 if fmt == "1x1" else 1130, 520 if fmt == "1x1" else 900)
    d = ImageDraw.Draw(im)
    texto_c(d, w, (985 if fmt == "1x1" else 1720), "2-YEAR WARRANTY  ·  FREE WORLDWIDE SHIPPING", fonte("sans", 26, 600), (200, 192, 180), espaco=2)
    return im


def t_ancora(fmt, prod):
    """C2: status / 'parece caro' sem citar marca de luxo (Pelvini 043, Laphont 'Is a name worth')."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h, (30, 30, 34), (3, 3, 5))
    d = ImageDraw.Draw(im)
    v = 1 if fmt == "1x1" else 1.6
    texto_c(d, w, 70 * v, "The $10K look.", fonte("serif", 96 if fmt == "1x1" else 112, 700), CREAM)
    colar_relogio(im, foto(prod), w / 2, 560 if fmt == "1x1" else 1000, 600 if fmt == "1x1" else 980)
    d = ImageDraw.Draw(im)
    yb = 900 if fmt == "1x1" else 1580
    texto_c(d, w, yb, "Without the $10K price tag.", fonte("serif", 54 if fmt == "1x1" else 64, 400), GOLD)
    marca(d, w, yb + (100 if fmt == "1x1" else 150), CREAM, 28)
    return im


def t_grade(fmt, prods, titulo="PICK ANY TWO", sub="THE SECOND ONE IS FREE"):
    """C8: grade de modelos (Lucky Fours 001/017, Mockberg 017)."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h, (22, 20, 18), (6, 6, 6))
    d = ImageDraw.Draw(im)
    cols, rows = (3, 2) if fmt == "1x1" else (2, 3)
    topo = 225 if fmt == "1x1" else 345
    rod = 120 if fmt == "1x1" else 230
    cw, ch = w / cols, (h - topo - rod) / rows
    texto_c(d, w, 50 if fmt == "1x1" else 90, titulo, fonte("anton", 92 if fmt == "1x1" else 120), CREAM)
    texto_c(d, w, 168 if fmt == "1x1" else 262, sub, fonte("sans", 28, 600), GOLD, espaco=3)
    for i, p in enumerate(prods[: cols * rows]):
        cx = cw * (i % cols) + cw / 2
        cy = topo + ch * (i // cols) + ch / 2
        colar_relogio(im, foto(p), cx, cy, ch * 0.92)
    d = ImageDraw.Draw(im)
    marca(d, w, h - rod + (40 if fmt == "1x1" else 80), (200, 192, 180), 28)
    return im


def t_catalogo(fmt, prod):
    """C9: moldura de catálogo (Pelvini 001: packshot + selo de oferta)."""
    w, h = FORMATOS[fmt]
    im = fundo(w, h, (20, 20, 20), (0, 0, 0))
    colar_relogio(im, foto(prod), w / 2, h / 2, h * 0.78 if fmt == "1x1" else w * 1.05)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 380, 150), radius=16, fill=GOLD)
    d.text((66, 52), "BUY 1", font=fonte("anton", 44), fill=INK)
    d.text((66, 98), "GET 1 FREE", font=fonte("anton", 40), fill=INK)
    faixa = 90
    d.rectangle((0, h - faixa, w, h), fill=(0, 0, 0))
    texto_c(d, w, h - faixa + 28, "FREE WORLDWIDE SHIPPING  ·  90-DAY RETURNS", fonte("sans", 26, 600), CREAM, espaco=2)
    return im


LOTE = [
    # (nome-base, função, args)
    ("C1_P2_bogo-caixa_verde-azul", t_bogo_caixa, ("vittorio", "pelvini-opulent")),
    ("C1_P2_bogo-caixa_ouro-prata", t_bogo_caixa, ("pelvini-lucent", "pelvini-maretti-1")),
    ("C1_P2_his-hers_milano-clovera", t_his_hers, ("pelvini-milano", "pelvini-clovera")),
    ("C1_P2_his-hers_titan-serafina", t_his_hers, ("titan", "pelvini-serafina")),
    ("C2_P1_ancora-10k_milano", t_ancora, ("pelvini-milano",)),
    ("C2_P1_ancora-10k_lucent", t_ancora, ("pelvini-lucent",)),
    ("C3_P3_generico-x-nos_vittorio", t_genericoxnos, ("vittorio",)),
    ("C3_P3_generico-x-nos_dante", t_genericoxnos, ("pelvini-dante",)),
    ("C4_P3_garantia-90d_opulent", t_garantia, ("pelvini-opulent",)),
    ("C4_P3_garantia-90d_titan", t_garantia, ("titan",)),
    ("C8_P2_grade-pick-two_homem", t_grade, (["vittorio", "pelvini-milano", "pelvini-opulent", "pelvini-maretti-1", "pelvini-dante", "pelvini-lucent"],)),
    ("C8_P5_grade-pick-two_mulher", t_grade, (["pelvini-clovera", "pelvini-serafina", "pelvini-lunetta", "pelvini-fiorella", "pelvini-grazia", "pelvini-aria"],)),
]
CATALOGO = ["vittorio", "pelvini-milano", "pelvini-opulent", "pelvini-maretti-1", "titan", "pelvini-dante",
            "pelvini-lucent", "pelvini-portofina", "pelvini-clovera", "pelvini-serafina", "pelvini-napoli", "pelvini-milano-ice"]

if __name__ == "__main__":
    n = 0
    for nome, fn, args in LOTE:
        for fmt in FORMATOS:
            fn(fmt, *args).save(os.path.join(SAIDA, f"{nome}_{fmt}.jpg"), quality=92)
            n += 1
    os.makedirs(os.path.join(SAIDA, "catalogo"), exist_ok=True)
    for p in CATALOGO:
        t_catalogo("1x1", p).save(os.path.join(SAIDA, "catalogo", f"C9_todas_catalogo-bogo_{p}_1x1.jpg"), quality=92)
        n += 1
    print(n, "imagens em", SAIDA)

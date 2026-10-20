# -*- coding: utf-8 -*-
"""4 estáticos do lote enxuto Lymphoria (1 por conceito C1, C2, C3, C5), 1080x1350.
Foto: Nano Banana 2 i2i (Flora) com o frasco n59 de referência; textos desenhados aqui (PIL), sem preço."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = Path(__file__).parent
IMGS = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\_trabalho\prod\IMGS")
sys.path.insert(0, str(IMGS))
import tx  # noqa: E402  (logo Lymphoria: folha + texto)

F = IMGS / "fonts"
OUT = Path(r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\LYMPHORIA-ENXUTO\IMAGENS")
W, H = 1080, 1350
VERDE = (25, 74, 52)
VERDE2 = (37, 104, 74)
CREME = (250, 245, 232)
AMAR = (255, 214, 0)
BRANCO = (255, 255, 255)
PRETO = (22, 22, 22)


def fnt(nome, px):
    return ImageFont.truetype(str(F / nome), px)


def quebra(d, txt, f, maxw):
    linhas, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            linhas.append(cur)
            cur = w
    linhas.append(cur)
    return linhas


def centro(d, y, txt, f, cor, maxw=960, gap=1.08, seco=False):
    for l in quebra(d, txt, f, maxw):
        w = d.textlength(l, font=f)
        if not seco:
            d.text(((W - w) / 2, y), l, font=f, fill=cor)
        y += int(f.size * gap)
    return y


def topo(im, blocos, y0=105, alpha=238):
    """Mede os blocos de texto, pinta a faixa creme até o fim do texto e escreve. blocos: [(txt, fonte, cor, kw)]."""
    d = ImageDraw.Draw(im)
    y = y0
    for txt, f, cor, kw in blocos:
        y = centro(d, y + kw.get("dy", 0), txt, f, cor, maxw=kw.get("maxw", 960), gap=kw.get("gap", 1.08), seco=True)
    painel_topo(im, y + 22, alpha)
    d = ImageDraw.Draw(im)
    tx.logo(im, (W // 2, 62), 40, VERDE2, anchor="m")
    y = y0
    for txt, f, cor, kw in blocos:
        y = centro(d, y + kw.get("dy", 0), txt, f, cor, maxw=kw.get("maxw", 960), gap=kw.get("gap", 1.08))
    return y


def foto(nome, dy=0):
    im = Image.open(AQUI / "img" / f"{nome}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = max(0, min(im.height - H, (im.height - H) // 2 + dy))
    return im.crop((x0, y0, x0 + W, y0 + H))


def painel_topo(im, h, alpha=235):
    """Faixa creme no topo com degradê para a foto."""
    ov = Image.new("RGBA", (W, h + 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(h + 90):
        a = alpha if y < h else int(alpha * (1 - (y - h) / 90))
        d.line((0, y, W, y), fill=CREME + (a,))
    im.paste(ov, (0, 0), ov)


def rodape(im, linha1, linha2, y=1150):
    d = ImageDraw.Draw(im)
    d.rectangle((0, y, W, H), fill=VERDE)
    f1, f2 = fnt("Poppins-Black.ttf", 64), fnt("Poppins-Bold.ttf", 34)
    w = d.textlength(linha1, font=f1)
    d.text(((W - w) / 2, y + 22), linha1, font=f1, fill=AMAR)
    w = d.textlength(linha2, font=f2)
    d.text(((W - w) / 2, y + 116), linha2, font=f2, fill=BRANCO)


def salvar(im, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / nome
    im.convert("RGB").save(p, quality=93)
    print("ok", p)


OFERTA = "COMPRE 1, RECIBA 2"
COD = "Pagas al recibir · Envío gratis · 90 días de garantía"


def c1():
    im = foto("c1", dy=0)
    topo(im, [("¿Llegas con los tobillos hinchados?", fnt("Poppins-Black.ttf", 82), VERDE, {"maxw": 980, "gap": 1.05}),
              ("Todo el día de pie… prueba Lymphoria: 4 hierbas y sabe a miel.", fnt("Poppins-Bold.ttf", 38), PRETO, {"dy": 6})])
    rodape(im, OFERTA, COD)
    salvar(im, "LYM-CL_C1_de-pie-todo-el-dia_estatico.jpg")


def c2():
    im = foto("c2", dy=60)
    topo(im, [("—¿Estás embarazada?", fnt("Poppins-Black.ttf", 84), VERDE, {"maxw": 1040}),
              ("—No… es hinchazón.", fnt("Poppins-Black.ttf", 66), (190, 40, 40), {"maxw": 1040}),
              ("¿Cansada de esa pregunta? Conoce Lymphoria.", fnt("Poppins-Bold.ttf", 38), PRETO, {"dy": 8})])
    rodape(im, OFERTA, COD)
    salvar(im, "LYM-CL_C2_pregunta-embarazada_estatico.jpg")


def c3():
    im = foto("c3", dy=-40)
    topo(im, [("«Volví a usar mis anillos»", fnt("DMSerifDisplay-Regular.ttf", 88), VERDE, {"maxw": 1040}),
              ("Para las que pasamos los 60: unas gotitas al día, 4 hierbas y adiós hinchazón.",
               fnt("Poppins-Bold.ttf", 36), PRETO, {"dy": 4})], alpha=245)
    rodape(im, OFERTA, COD)
    d = ImageDraw.Draw(im)
    f = fnt("Poppins-Bold.ttf", 22)
    t = "*Imagen ilustrativa. Los resultados pueden variar según cada persona."
    w = d.textlength(t, font=f)
    d.text(((W - w) / 2, 1112), t, font=f, fill=BRANCO, stroke_width=2, stroke_fill=(0, 0, 0))
    salvar(im, "LYM-CL_C3_jubilada-anillos_estatico.jpg")


def c5():
    im = foto("c5", dy=40)
    painel_topo(im, 330, alpha=240)
    d = ImageDraw.Draw(im)
    tx.logo(im, (W // 2, 58), 40, VERDE2, anchor="m")
    y = centro(d, 92, "PAGAS AL RECIBIR", fnt("Poppins-Black.ttf", 112), VERDE, maxw=1040, gap=1.0)
    passos = ["1. Pides", "2. Te llega gratis", "3. Recién ahí pagas"]
    f = fnt("Poppins-Bold.ttf", 36)
    ws = [d.textlength(p, font=f) + 48 for p in passos]
    gap = 16
    x = (W - sum(ws) - gap * 2) / 2
    y += 18
    for p, w in zip(passos, ws):
        d.rounded_rectangle((x, y, x + w, y + 64), 32, fill=VERDE2)
        d.text((x + 24, y + 10), p, font=f, fill=BRANCO)
        x += w + gap
    centro(d, y + 84, "Sin tarjeta y sin adelantar ni un peso.", fnt("Poppins-Bold.ttf", 36), PRETO)
    rodape(im, OFERTA, "Envío gratis a todo Chile · 90 días de garantía")
    salvar(im, "LYM-CL_C5_desconfiada-online_estatico.jpg")


if __name__ == "__main__":
    for fn in (sys.argv[1:] or ["c1", "c2", "c3", "c5"]):
        globals()[fn]()

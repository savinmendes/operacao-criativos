# -*- coding: utf-8 -*-
"""Overlays do agente B (kit hombre 3 en 1, COD Chile, SEM PREÇO). 720x1280, PIL, sem custo.
banner_topo.png (selo PAGO CONTRA ENTREGA · ENVÍO EN 24 HORAS, cobre o selo queimado do vencedor),
sticker_kit.png (card preto com os 3 frascos, cobre o sticker queimado do rodapé), titulo_04/05/06.png, cta_final.png."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, r"C:\Users\PICHAU\Downloads\YARA-CL\producao\edicao\_trabalho")
import gerar_overlays_sem_preco as g  # noqa: E402

OUT = Path(__file__).resolve().parent
N2 = Path(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\flora\image_n2.png")
W, H = 720, 1280
NAVY = (18, 42, 82, 255)
F, PB, PS, AN = g.F, g.PB, g.PS, g.AN


def frascos():
    im = Image.open(N2).convert("RGB")
    import numpy as np
    a = np.asarray(im).astype(int)
    # fundo branco -> alfa (distância do branco), com borda suave
    d = (255 - a).max(axis=2)
    alpha = np.clip((d - 8) * 12, 0, 255).astype("uint8")
    rgba = Image.fromarray(np.dstack([a.astype("uint8"), alpha]), "RGBA")
    # preenche buracos internos (vidro claro do 9pm): fecha a máscara por componentes
    from scipy import ndimage
    m = alpha > 40
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, iterations=3))
    al = np.maximum(alpha, (m * 255).astype("uint8"))
    rgba.putalpha(Image.fromarray(al))
    return rgba.crop(rgba.getbbox())


def banner():
    w, h, S = 510, 96, 3
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((-40 * S, 0, w * S - 1, h * S - 1), 22 * S, fill=NAVY)
    d.text((26 * S, 16 * S), "PAGO CONTRA ENTREGA", font=F(PS, 27 * S), fill=(255, 255, 255, 255))
    d.text((26 * S, 52 * S), "ENVÍO EN 24 HORAS", font=F(PB, 23 * S), fill=(255, 214, 0, 255))
    # caminhão simples
    x0, y0 = 392 * S, 26 * S
    br = (255, 255, 255, 255)
    d.rounded_rectangle((x0, y0, x0 + 58 * S, y0 + 36 * S), 4 * S, fill=br)
    d.polygon([(x0 + 60 * S, y0 + 10 * S), (x0 + 80 * S, y0 + 10 * S), (x0 + 92 * S, y0 + 24 * S),
               (x0 + 92 * S, y0 + 36 * S), (x0 + 60 * S, y0 + 36 * S)], fill=br)
    d.rectangle((x0 + 66 * S, y0 + 14 * S, x0 + 80 * S, y0 + 22 * S), fill=NAVY)
    for cx in (x0 + 16 * S, x0 + 76 * S):
        d.ellipse((cx - 9 * S, y0 + 30 * S, cx + 9 * S, y0 + 48 * S), fill=br)
        d.ellipse((cx - 4 * S, y0 + 35 * S, cx + 4 * S, y0 + 43 * S), fill=NAVY)
    for i, yy in enumerate((y0 + 6 * S, y0 + 16 * S, y0 + 26 * S)):
        d.rectangle((x0 - (22 - 4 * i) * S, yy, x0 - 6 * S, yy + 3 * S), fill=br)
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / "banner_topo.png")
    return im


def sticker(fr):
    w, h = 480, 345
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(12, 12, 12, 250), outline=g.OURO, width=3)
    im.alpha_composite(card)
    pw = w - 40
    f2 = fr.resize((pw, int(fr.height * pw / fr.width)), Image.LANCZOS)
    if f2.height > h - 24:
        ph = h - 24
        f2 = fr.resize((int(fr.width * ph / fr.height), ph), Image.LANCZOS)
    im.alpha_composite(f2, ((w - f2.width) // 2, (h - f2.height) // 2))
    im.save(OUT / "sticker_kit.png")
    return im


def novo():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def cx(im, el, y):
    im.alpha_composite(el, ((W - el.width) // 2, int(y)))
    return int(y) + el.height


def caber(el, maxw=690):
    return el if el.width <= maxw else el.resize((maxw, int(el.height * maxw / el.width)), Image.LANCZOS)


def titulos():
    im = novo()
    y = cx(im, caber(g.faixa_texto("¿QUÉ PERFUME USAS?", AN, 84, g.OURO, g.PRETO, padx=20, pady=7, angulo=2,
                                     contorno=g.OURO)), 60)
    im.save(OUT / "titulo_04.png")
    im = novo()
    y = cx(im, caber(g.faixa_texto("¿QUÉ PERFUME ANDAI TRAYENDO?", AN, 66, g.OURO, g.PRETO, padx=18, pady=7,
                                     angulo=-2, contorno=g.OURO)), 60)
    im.save(OUT / "titulo_06.png")
    im = novo()
    y = cx(im, caber(g.texto_contorno("¿PERFUME POR INTERNET?", AN, 70, g.BRANCO, sw=7, angulo=-2)), 50)
    cx(im, caber(g.faixa_texto("¿Y SI NO LLEGA?", AN, 92, g.BRANCO, g.VERM, padx=20, pady=6, angulo=-2)), y - 6)
    im.save(OUT / "titulo_05.png")


def cta(fr):
    im = Image.new("RGBA", (W, H), g.PRETO)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((60, 560, 660, 1160), fill=(232, 186, 74, 100))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, W - 25, H - 25), outline=g.OURO, width=3)
    t1 = g.texto_contorno("3 PERFUMES", AN, 128, g.BRANCO, sw=0)
    y = cx(im, t1, 110)
    t2 = g.texto_contorno("AL PRECIO DE 1", AN, 96, g.OURO2, sw=0)
    y = cx(im, t2, y - 18)
    d = ImageDraw.Draw(im)
    g.centro(d, "Club de Nuit · Asad · 9PM", F(PB, 38), y + 8, g.BRANCO, W / 2)
    pill_y = y + 76
    d.rounded_rectangle((50, pill_y, W - 50, pill_y + 80), 24, fill=g.OURO)
    g.centro(d, "PAGAS AL RECIBIR", F(PB, 40), pill_y + 13, g.PRETO, W / 2)
    g.centro(d, "Envío en 24 horas", F(PS, 32), pill_y + 100, g.BRANCO, W / 2)
    # frascos no rodapé
    pw = 640
    f2 = fr.resize((pw, int(fr.height * pw / fr.width)), Image.LANCZOS)
    im.alpha_composite(f2, ((W - pw) // 2, H - 40 - f2.height))
    print("cta: pill termina", pill_y + 80, "| frascos de", H - 40 - f2.height)
    im.convert("RGB").save(OUT / "cta_final.png")
    return im


if __name__ == "__main__":
    fr = frascos()
    b = banner(); s = sticker(fr); titulos(); c = cta(fr)
    # preview sobre um quadro do vencedor
    q = Image.open(OUT.parent / "ref" / "v329_25.png").convert("RGBA")
    a = q.copy(); a.alpha_composite(b, (0, 22)); a.alpha_composite(s, ((W - s.width) // 2, H - s.height - 40))
    p = Image.new("RGB", (W * 5, H), (60, 60, 60))
    p.paste(a.convert("RGB"), (0, 0))
    for i, n in enumerate(["titulo_04.png", "titulo_05.png", "titulo_06.png"]):
        bg = Image.open(OUT.parent / "imagens" / "I4_homemB_sofa.png").convert("RGBA").resize((W, H))
        bg.alpha_composite(Image.open(OUT / n)); p.paste(bg.convert("RGB"), (W * (i + 1), 0))
    p.paste(c.convert("RGB"), (W * 4, 0))
    p.save(OUT / "_preview.jpg")

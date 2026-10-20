# -*- coding: utf-8 -*-
"""Título novo do quadro das 12 palavras (placa verde-escura com moldura dourada) + círculos vermelhos por palavra."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = Path(__file__).resolve().parent; W, H = 720, 1280; WF = Path(r"C:\Windows\Fonts")
BOX = (138, 160, 592, 330)
PAL = ["Cruz", "Lux", "Fides", "Ignes", "Veritas", "Silentio", "Gladius", "Fortitudo", "Custodia", "Sanctitas", "Spiritus", "Triumphus"]
CEN = [(360, 383), (226, 438), (494, 438), (140, 545), (581, 545), (117, 652), (603, 652), (152, 762), (569, 762), (225, 866), (360, 895), (497, 866)]

def grad(w, h, c0, c1):
    g = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1); d.line([(0, y), (w, y)], fill=tuple(int(c0[i] * (1 - t) + c1[i] * t) for i in range(3)) + (255,))
    return g

def texto_ouro(im, cx, cy, txt, tam, sx=0.86):
    f = ImageFont.truetype(str(WF / "cambriab.ttf"), tam)
    tmp = Image.new("L", (1400, 300), 0); d = ImageDraw.Draw(tmp); d.text((700, 150), txt, font=f, fill=255, anchor="mm")
    bb = tmp.getbbox(); m = tmp.crop(bb); m = m.resize((int(m.size[0] * sx), m.size[1]), Image.LANCZOS)
    w, h = m.size; x, y = int(cx - w / 2), int(cy - h / 2)
    # sombra + contorno escuro
    cont = m.filter(ImageFilter.MaxFilter(5)); sh = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    sh.paste((20, 10, 0, 255), (10, 10), cont); sh = sh.filter(ImageFilter.GaussianBlur(3))
    im.alpha_composite(sh, (x - 8, y - 6))
    c2 = Image.new("RGBA", (w, h), (45, 25, 5, 255)); im.paste(c2, (x, y), cont)
    ouro = grad(w, h, (255, 240, 185), (196, 140, 58)); im.paste(ouro, (x, y), m)

def titulo():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x0, y0, x1, y1 = BOX
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0 - 2, y0 + 4, x1 + 2, y1 + 8], 14, fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    pl = grad(x1 - x0, y1 - y0, (24, 46, 30), (9, 20, 12)); m = Image.new("L", pl.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, pl.size[0] - 1, pl.size[1] - 1], 14, fill=255); im.paste(pl, (x0, y0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], 14, outline=(214, 170, 82, 255), width=4)
    d.rounded_rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 8], 9, outline=(160, 118, 48, 255), width=2)
    for cx, cy in [(x0 + 8, y0 + 8), (x1 - 8, y0 + 8), (x0 + 8, y1 - 8), (x1 - 8, y1 - 8)]:
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(226, 184, 96, 255), outline=(120, 80, 20, 255))
    d.polygon([((x0 + x1) / 2, y0 - 12), ((x0 + x1) / 2 + 12, y0), ((x0 + x1) / 2, y0 + 12), ((x0 + x1) / 2 - 12, y0)], fill=(226, 184, 96, 255), outline=(120, 80, 20, 255))
    texto_ouro(im, 365, y0 + 42, "Las 12 Palabras", 40)
    texto_ouro(im, 365, y0 + 88, "Sagradas de", 40)
    texto_ouro(im, 365, y0 + 136, "San Benito", 50)
    im.save(AQ / "board_titulo.png")

def circulo(k, frac=1.0):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx, cy = CEN[k]; a, b = 66, 56
    d.arc([cx - a, cy - b, cx + a, cy + b], -100, -100 + 360 * frac, fill=(222, 28, 40, 255), width=4)
    return im

if __name__ == "__main__":
    titulo()
    for k in range(12):
        for j, fr in enumerate((0.3, 0.6, 0.85, 1.0)): circulo(k, fr).save(AQ / f"circ_{k:02d}_{j}.png")
    base = Image.open(AQ.parent / "q" / "board_clean.png").convert("RGBA"); base.alpha_composite(Image.open(AQ / "board_titulo.png"))
    for k in range(12): base.alpha_composite(circulo(k))
    base.save(AQ.parent / "q" / "board_prev.png"); print("ok")

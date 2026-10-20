# -*- coding: utf-8 -*-
"""Gera os PNGs de texto grande (720x1280, transparente) do F5 Sensorial."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import overlays as OV
ANTON = str(KIT / "fonts" / "Anton-Regular.ttf"); POP = str(KIT / "fonts" / "Poppins-Bold.ttf")
OUT = Path(__file__).parent / "txt"; OUT.mkdir(exist_ok=True)
W, H = 720, 1280
GOLD, WHITE = (245, 196, 82, 255), (255, 255, 255, 255)

def camada(itens, nome):
    """itens: [(texto, fonte_path, px, cor, y_centro_topo, visivel)]; sombra + contorno."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for txt, fp, px, cor, y, vis in itens:
        if not vis: continue
        f = ImageFont.truetype(fp, px)
        if "👃" in txt or "🔥" in txt:
            base = txt.replace(" 👃", "").replace(" 🔥", "")
            em = txt[len(base):]
            wtot = f.getlength(base) + (px * 1.05 if em else 0)
            x = (W - wtot) / 2
            ImageDraw.Draw(sombra).text((x + 4, y + 6), base, font=f, fill=(0, 0, 0, 230))
            ImageDraw.Draw(img).text((x, y), base, font=f, fill=cor, stroke_width=max(3, px // 22), stroke_fill=(0, 0, 0, 255))
            OV._desenha_linha(img, (x + f.getlength(base) + 10, y - px * 0.05), em.strip(), f)
        else:
            x = (W - f.getlength(txt)) / 2
            ImageDraw.Draw(sombra).text((x + 4, y + 6), txt, font=f, fill=(0, 0, 0, 230))
            ImageDraw.Draw(img).text((x, y), txt, font=f, fill=cor, stroke_width=max(3, px // 22), stroke_fill=(0, 0, 0, 255))
    sombra = sombra.filter(ImageFilter.GaussianBlur(8))
    out = Image.alpha_composite(sombra, img)
    out.save(OUT / f"{nome}.png")

# gancho
camada([("¿A QUÉ HUELES", ANTON, 96, WHITE, 960, True), ("TÚ? 👃", ANTON, 96, GOLD, 1075, True)], "t00_gancho")
# perfumes: nome + 3 adjetivos que entram um a um
P = {"armaf": ("ARMAF", ["FRESCO", "MASCULINO", "PODEROSO"]),
     "asad": ("ASAD", ["INTENSO", "SOFISTICADO", "SEDUCTOR"]),
     "9pm": ("9PM", ["ELEGANTE", "MODERNO", "REFINADO"])}
for k, (nome, adj) in P.items():
    for n in range(4):
        itens = [(nome, ANTON, 130, GOLD, 122, True)]
        # adjetivos numa linha só, separados por ·, só os n primeiros visíveis (posição fixa)
        f = ImageFont.truetype(ANTON, 50)
        linha = " · ".join(adj)
        x0 = (W - f.getlength(linha)) / 2
        img_itens = []
        pos = x0
        partes = []
        for i, a in enumerate(adj):
            partes.append((a, pos, i < n))
            pos += f.getlength(a + " · ")
        camada(itens, f"_tmp")
        im = Image.open(OUT / "_tmp.png")
        d = ImageDraw.Draw(im)
        for i, (a, px_, vis) in enumerate(partes):
            if not vis: continue
            d.text((px_, 296), a, font=f, fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0, 255))
            if i < len(partes) - 1 and partes[i + 1][2]:
                d.text((px_ + f.getlength(a + " "), 296), "·", font=f, fill=GOLD, stroke_width=3, stroke_fill=(0, 0, 0, 255))
        im.save(OUT / f"t_{k}_{n}.png")
(OUT / "_tmp.png").unlink()
# fecho
camada([("3 PERFUMES", ANTON, 112, WHITE, 120, True), ("AL PRECIO DE 1", ANTON, 84, GOLD, 255, True)], "t90_oferta")
camada([("3 PERFUMES", ANTON, 112, WHITE, 120, True), ("AL PRECIO DE 1", ANTON, 84, GOLD, 255, True),
        ("PAGAS AL RECIBIR", ANTON, 84, WHITE, 935, True), ("ENVÍO EN 24 HORAS", ANTON, 52, GOLD, 1045, True)], "t91_cta")
OV.seta(str(OUT / "seta.png"), tam=110)
print("ok", sorted(p.name for p in OUT.glob("*.png")))

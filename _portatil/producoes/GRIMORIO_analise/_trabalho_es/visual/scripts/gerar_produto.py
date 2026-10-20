# -*- coding: utf-8 -*-
"""Tela do produto (substitui os prints do perfil): livro "Grimorio Sagrado y Secreto de San Benito" (capa do img0 com
título trocado) + colar (img4), "+ collar de regalo", "TOCA AQUÍ ABAJO" e seta. Sem preço/domínio/perfil.
Topo (y<112) transparente para a moldura da live aparecer."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
AQ = Path(__file__).resolve().parent.parent; T = AQ / "_tmp"; O = AQ / "overlays"
COL = Path(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\colar")
F = "C:/Windows/Fonts/"
def ouro(txt, font, size_box):
    """texto dourado com leve gradiente + sombra escura"""
    W, H = size_box
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m); d.text((W // 2, H // 2), txt, font=font, anchor="mm", fill=255)
    g = np.linspace(0, 1, H)[:, None]
    c1, c2 = np.array([246, 214, 140]), np.array([186, 136, 60])
    rgb = (c1[None, None] * (1 - g[..., None]) + c2[None, None] * g[..., None]).repeat(W, 1).astype(np.uint8)
    im = Image.fromarray(rgb).convert("RGBA"); im.putalpha(m)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(1.5)).point(lambda v: v * 0.8))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); out.alpha_composite(sh, (1, 2)); out.alpha_composite(im)
    return out
# ---- livro ----
bk = Image.open(T / "book_limpo.png").convert("RGBA")
for txt, fn, sz, cy in [("GRIMORIO", "cambriab.ttf", 58, 152), ("SAGRADO Y SECRETO", "cambriab.ttf", 28, 205), ("DE SAN BENITO", "cambriab.ttf", 40, 258)]:
    t = ouro(txt, ImageFont.truetype(F + fn, sz), (330, 70)); bk.alpha_composite(t, (281 - 165, cy - 35))
bk = bk.crop((60, 55, 500, 640)); bk.save(T / "book_es.png")
# ---- tela ----
W, H = 720, 1280
bg = Image.new("RGB", (W, H), (16, 12, 10))
g = np.linspace(0, 1, H)[:, None, None]; arr = (np.array([40, 28, 18]) * (1 - g) + np.array([10, 8, 6]) * g).repeat(W, 1)
yy, xx = np.mgrid[0:H, 0:W]; vig = 1 + 0.9 * np.exp(-(((xx - 360) / 330) ** 2 + ((yy - 470) / 380) ** 2))
bg = Image.fromarray(np.clip(arr * vig[..., None], 0, 255).astype(np.uint8)).convert("RGBA")
b = bk.resize((int(bk.width * 0.95), int(bk.height * 0.95)), Image.LANCZOS)
fm = np.ones((b.height, b.width), np.float32)
for k in range(45):
    v = k / 45; fm[k, :] = np.minimum(fm[k, :], v); fm[:, k] = np.minimum(fm[:, k], v); fm[:, -1 - k] = np.minimum(fm[:, -1 - k], v); fm[-1 - k, :] = np.minimum(fm[-1 - k, :], v)
b.putalpha(Image.fromarray((fm * 255).astype(np.uint8)))
bg.alpha_composite(b, (20, 122))
col = Image.open(COL / "img4.jpg").convert("RGB")      # colar na madeira
s = 330; col = col.resize((s, s), Image.LANCZOS)
mk = Image.new("L", (s, s), 0); ImageDraw.Draw(mk).ellipse((6, 6, s - 6, s - 6), fill=255); mk = mk.filter(ImageFilter.GaussianBlur(3))
ring = Image.new("RGBA", (s + 16, s + 16), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((0, 0, s + 15, s + 15), fill=(214, 170, 90, 255))
sh = Image.new("RGBA", (s + 60, s + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((20, 26, s + 40, s + 46), fill=(0, 0, 0, 170)); sh = sh.filter(ImageFilter.GaussianBlur(12))
cx, cy = 505, 515
bg.alpha_composite(sh, (cx - s // 2 - 30, cy - s // 2 - 30)); bg.alpha_composite(ring, (cx - s // 2 - 8, cy - s // 2 - 8))
c = col.convert("RGBA"); c.putalpha(mk); bg.alpha_composite(c, (cx - s // 2, cy - s // 2))
# selo "+ collar de regalo"
lab = ouro("+ COLLAR DE REGALO", ImageFont.truetype(F + "cambriab.ttf", 34), (420, 60))
pill = Image.new("RGBA", (380, 58), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, 379, 57), 28, fill=(120, 20, 20, 235), outline=(214, 170, 90, 255), width=3)
bg.alpha_composite(pill, (cx - 190 + 0, cy + s // 2 + 6)); bg.alpha_composite(lab, (cx - 210, cy + s // 2 + 5))
# TOCA AQUÍ ABAJO (abaixo da faixa da legenda, y~800)
f = ImageFont.truetype(F + "seguibl.ttf" if Path(F + "seguibl.ttf").exists() else F + "segoeuib.ttf", 64)
tx = Image.new("RGBA", (W, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
d.text((W // 2, 60), "TOCA AQUÍ ABAJO", font=f, anchor="mm", fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
bg.alpha_composite(tx, (0, 905))
bg = bg.convert("RGBA"); a = np.array(bg); a[:112, :, 3] = 0
a[112:124, :, 3] = (np.linspace(0, 255, 12)[:, None]).astype(np.uint8)
Image.fromarray(a).save(O / "produto_es.png")
# seta vermelha para baixo (animada pelo AUDIO com overlay y oscilando)
s2 = Image.new("RGBA", (200, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(s2)
poly = [(70, 0), (130, 0), (130, 110), (185, 110), (100, 210), (15, 110), (70, 110)]
d.polygon(poly, fill=(230, 20, 20, 255), outline=(255, 255, 255, 255), width=6)
s2.save(O / "seta_baixo.png")
prev = Image.fromarray(a).copy(); prev.alpha_composite(s2, (260, 1035)); prev.save(T / "produto_prev.png")
print("ok")

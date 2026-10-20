# -*- coding: utf-8 -*-
"""Sobreposições do V04: título de abertura, BLOQUEADO, FORMA CORRECTA, VIDEO ELIMINADO (moldura/selo/EN VIVO/TOCA/seta vêm do lote anterior)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; O = P / "ov"
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
def pf(s, w="ExtraBold"): return ImageFont.truetype(str(POP / f"Poppins-{w}.ttf"), s)
def sombra(im, r=6, a=170):
    al = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * a / 255))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(al); out = Image.new("RGBA", im.size); out.alpha_composite(sh, (0, 4)); out.alpha_composite(im); return out
# título (3 linhas, caixa escura translúcida, "900 AÑOS" amarelo)
f = pf(50); L = [("LA ORACIÓN QUE", None), ("ESCONDIERON DE TI", None), ("POR ", "900 AÑOS")]
W, H = 720, 250; im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((30, 6, 690, 244), 22, fill=(0, 0, 0, 200))
for k, (a, b) in enumerate(L):
    y = 50 + k * 74; tw = f.getlength(a) + (f.getlength(b) if b else 0); x = 360 - tw / 2
    d.text((x, y), a, font=f, fill=(255, 255, 255, 255), anchor="lm")
    if b: d.text((x + f.getlength(a), y), b, font=f, fill=(255, 214, 0, 255), anchor="lm")
im.save(O / "titulo.png")
# palavras gigantes
def gigante(linhas, cor, nome, tam):
    fg = pf(tam); hh = int(tam * 1.15); im = Image.new("RGBA", (720, hh * len(linhas) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, t in enumerate(linhas):
        s = tam; ff = fg
        while ff.getlength(t) > 680: s -= 4; ff = pf(s)
        d.text((360, 20 + hh * k + hh // 2), t, font=ff, anchor="mm", fill=cor, stroke_width=7, stroke_fill=(0, 0, 0, 255))
    sombra(im).save(O / nome)
gigante(["BLOQUEADO"], (235, 30, 30, 255), "bloqueado.png", 120)
gigante(["FORMA", "CORRECTA"], (255, 214, 0, 255), "forma_correcta.png", 118)
# VIDEO ELIMINADO (carimbo vermelho, levemente inclinado)
fs = pf(76); t1, t2 = "VIDEO", "ELIMINADO"; w = int(max(fs.getlength(t1), fs.getlength(t2))) + 90; h = 230
st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
d.rounded_rectangle((6, 6, w - 7, h - 7), 18, fill=(0, 0, 0, 150), outline=(235, 25, 25, 255), width=10)
d.text((w // 2, 72), t1, font=fs, anchor="mm", fill=(235, 25, 25, 255)); d.text((w // 2, 158), t2, font=fs, anchor="mm", fill=(235, 25, 25, 255))
st = st.rotate(-7, expand=True, resample=Image.BICUBIC); sombra(st, 8, 140).save(O / "eliminado.png")
for n in ("titulo", "bloqueado", "forma_correcta", "eliminado"): print(n, Image.open(O / f"{n}.png").size)

# -*- coding: utf-8 -*-
"""Sobreposições do Ranking 04 (720x1280): reaproveita do R02 TRANSMISIÓN ELIMINADA, EN VIVO, TOCA, seta, selo 10% e a moldura
da live «padre.juanmendez» (só no trecho EN VIVO); cria o rótulo TESTIMONIO e a moldura do PIP da apresentadora."""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; O = P / "ov"; O.mkdir(exist_ok=True)
R2 = P.parents[1] / "_analise_02" / "producao" / "ov"
for n in ("eliminado.png", "en_vivo.png", "toca.png", "seta.png", "moldura_jm.png"): shutil.copy(R2 / n, O / n)
shutil.copy(Path(r"C:\Users\PICHAU\Downloads\SB-ES_PADRE-CAPTURADO\corpo\_trab\ov\selo10.png"), O / "selo10.png")
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
def sombra(im, r=6, a=150, dy=4):
    al = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * a / 255))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(al); out = Image.new("RGBA", im.size); out.alpha_composite(sh, (0, dy)); out.alpha_composite(im); return out
f = ImageFont.truetype(str(POP / "Poppins-ExtraBold.ttf"), 34); t = "TESTIMONIO"; w = int(f.getlength(t)) + 44
im = Image.new("RGBA", (w + 20, 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((10, 10, w + 10, 70), 12, fill=(205, 12, 16, 255)); d.text((10 + w / 2, 40), t, font=f, anchor="mm", fill=(255, 255, 255, 255))
sombra(im).save(O / "testimonio.png")
# PIP da apresentadora: caixa 44..704 x 600..1110, borda branca
X0, Y0, X1, Y1, R = 44, 600, 704, 1110, 26
m = Image.new("L", (720, 1280), 0); ImageDraw.Draw(m).rounded_rectangle((X0, Y0, X1, Y1), R, fill=255); m.save(O / "pip_mask.png")
b = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ImageDraw.Draw(b).rounded_rectangle((X0 - 2, Y0 - 2, X1 + 2, Y1 + 2), R + 2, outline=(255, 255, 255, 255), width=5)
sh = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((X0, Y0 + 8, X1, Y1 + 8), R, fill=(0, 0, 0, 120))
out = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); out.save(O / "pip_sombra.png"); b.save(O / "pip_borda.png")
print("ok")

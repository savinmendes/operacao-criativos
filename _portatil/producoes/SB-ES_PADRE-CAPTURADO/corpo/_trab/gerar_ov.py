# -*- coding: utf-8 -*-
"""Sobreposições novas: título do gancho (Juan Méndez), selo (cópia do v4), selo EN VIVO, texto TOCA EN «VER MÁS», seta (kit), molde do badge da arroba."""
import sys, shutil, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T = Path(__file__).resolve().parent; O = T / "ov"
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
VIS = Path(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\visual\overlays")
def osf(sz, w="Regular"):
    f = ImageFont.truetype(OS, sz); f.set_variation_by_name(w); return f
# 1) título (mesmo desenho do gerar_titulo_selo.py do v4)
f = osf(44)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.rectangle((0, 128, 719, 248), fill=(0, 0, 0, 255))
L = Image.new("L", (720, 1280), 0); dl = ImageDraw.Draw(L)
dl.text((360, 184), "EL PADRE JUAN MÉNDEZ LO VA A", font=f, anchor="ms", fill=255)
dl.text((360, 230), "REVELAR TODO EN VIVO", font=f, anchor="ms", fill=255)
L = L.filter(ImageFilter.GaussianBlur(0.4))
im.alpha_composite(Image.composite(Image.new("RGBA", (720, 1280), (188, 202, 20, 255)), Image.new("RGBA", (720, 1280), (0, 0, 0, 0)), L))
im.save(O / "titulo_gancho_jm.png")
shutil.copy(VIS / "selo_ficticio_mini_es.png", O / "selo.png")
# 2) EN VIVO (bolinha vermelha desenhada + texto), sem cara de botão: pílula escura translúcida
fp = ImageFont.truetype(str(POP / "Poppins-Bold.ttf"), 46)
t = "EN VIVO"; tw = fp.getlength(t); r = 15; pad = 26; gap = 16
W = int(pad + 2 * r + gap + tw + pad); H = 78
ev = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ev)
d.rounded_rectangle((0, 0, W - 1, H - 1), 20, fill=(0, 0, 0, 165))
cy = H // 2; d.ellipse((pad, cy - r, pad + 2 * r, cy + r), fill=(235, 20, 20, 255), outline=(255, 255, 255, 255), width=3)
d.text((pad + 2 * r + gap, cy + 1), t, font=fp, anchor="lm", fill=(255, 255, 255, 255))
ev.save(O / "en_vivo.png"); print("en_vivo", ev.size)
# 3) TOCA EN «VER MÁS» (texto grande, contorno preto, sem caixa)
fc = ImageFont.truetype(str(POP / "Poppins-ExtraBold.ttf"), 54)
tx = "TOCA EN «VER MÁS»"; w = int(fc.getlength(tx)) + 40
ct = Image.new("RGBA", (w, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(ct)
d.text((w // 2, 45), tx, font=fc, anchor="mm", fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
ct.save(O / "toca.png"); print("toca", ct.size)
# 4) seta do kit (escala 2/3 para 720)
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import overlays as OV
OV.seta(str(O / "seta.png"), escala=2 / 3); print("seta", Image.open(O / "seta.png").size)

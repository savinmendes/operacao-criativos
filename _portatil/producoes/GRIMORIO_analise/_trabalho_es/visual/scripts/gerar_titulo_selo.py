# -*- coding: utf-8 -*-
"""Título amarelo ES do gancho (cobre o PT com faixa preta opaca) + selo VIDEO FICTICIO mini (texto ES)."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent.parent; O = AQ / "overlays"; O.mkdir(exist_ok=True)
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
def fonte(sz):
    f = ImageFont.truetype(OS, sz); f.set_variation_by_name("Regular"); return f
# tamanho que reproduz a largura da linha 2 original ("REVELAR TUDO AO VIVO" = 494 px)
sz = min(range(36, 52), key=lambda s: abs(fonte(s).getbbox("REVELAR TUDO AO VIVO")[2] - fonte(s).getbbox("REVELAR TUDO AO VIVO")[0] - 494))
f = fonte(sz); print("Open Sans Regular", sz)
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rectangle((0, 128, 719, 248), fill=(0, 0, 0, 255))
L = Image.new("L", (720, 1280), 0); dl = ImageDraw.Draw(L)
# baselines das linhas originais: caixas 153–184 e 198–230 (maiúsculas) -> baseline 184 e 230
dl.text((360, 184), "EL PADRE PABLO LO VA A", font=f, anchor="ms", fill=255)
dl.text((360, 230), "REVELAR TODO EN VIVO", font=f, anchor="ms", fill=255)
L = L.filter(ImageFilter.GaussianBlur(0.4))
im.alpha_composite(Image.composite(Image.new("RGBA", (720, 1280), (188, 202, 20, 255)), Image.new("RGBA", (720, 1280), (0, 0, 0, 0)), L))
im.save(O / "titulo_gancho_es.png")
# selo mini (mesmo desenho do gerar_selo_pt.py, texto ES)
FON = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
W, H = 1080, 1920
s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
fp = ImageFont.truetype(str(FON / "Poppins-Bold.ttf"), 18); t = "VIDEO FICTICIO"
b = d.textbbox((0, 0), t, font=fp); w, h = b[2] - b[0], b[3] - b[1]
px, py = 11, 6; x1 = W - 20; x0 = x1 - w - 2 * px; y0 = 4; y1 = y0 + h + 2 * py
d.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=(0, 0, 0, 179))
d.text((x0 + px - b[0], y0 + py - b[1]), t, font=fp, fill=(255, 255, 255, 255))
s.resize((720, 1280), Image.LANCZOS).save(O / "selo_ficticio_mini_es.png")
print("selo caixa 720:", [round(v * 2 / 3, 1) for v in (x0, y0, x1, y1)])

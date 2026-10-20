# -*- coding: utf-8 -*-
"""Troca a arroba da moldura da live: 'padre.pablo_' + selo azul -> 'padre.juanmendez' + selo azul.
Fundo (madeira com listras verticais) refeito por interpolação vertical coluna a coluna; força pela presença do texto antigo."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
T = Path(__file__).resolve().parent
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
REF = np.asarray(Image.open(T / "f700.png").convert("RGB"))
X0, X1, Y0, Y1 = 182, 446, 50, 92            # área apagada
TXM = REF[55:88, 188:356].min(2) > 150        # pixels do texto antigo (sem o selo)
ANM = REF[55:88, 188:356].min(2) < 90
SC_REF = float(REF[55:88, 188:356].min(2)[TXM].mean() - REF[55:88, 188:356].min(2)[ANM].mean())
# selo azul: círculo em (372,62) r~9
yy, xx = np.mgrid[0:24, 0:24]; dist = np.sqrt((yy - 11.5) ** 2 + (xx - 11.5) ** 2)
BA = np.clip(9.6 - dist, 0, 1)[..., None]; BADGE = REF[62 - 12 + 0:62 + 12, 372 - 12:372 + 12].astype(np.float32)
# texto novo (supersample 2x)
f2 = ImageFont.truetype(OS, 52); f2.set_variation_by_name("SemiBold")
TXT = "padre.juanmendez"
Lb = Image.new("L", (1440, 200), 0); ImageDraw.Draw(Lb).text((2 * 186.5, 2 * 79 - 2 * 40), TXT, font=f2, anchor="ls", fill=255)
TL = np.asarray(Lb.resize((720, 100), Image.LANCZOS)).astype(np.float32)[None] / 255   # linhas 40..140
TL = TL[0]
x_fim = 186.5 + f2.getlength(TXT) / 2
BX = int(round(x_fim + 21)); BY = 62 - 12
COR = np.percentile(REF[55:88, 188:356][TXM], 90, axis=0).astype(np.float32)
def forca(f):
    m = f[55:88, 188:356].min(2).astype(np.float32)
    sc = float(m[TXM].mean() - m[ANM].mean())
    return float(np.clip((sc / SC_REF - 0.25) / 0.6, 0, 1))
def aplica(f):
    a = forca(f)
    if a <= 0: return f
    o = f.astype(np.float32).copy()
    top = o[Y0 - 4:Y0].mean(0); bot = o[Y1:Y1 + 4].mean(0)
    w = np.linspace(0, 1, Y1 - Y0)[:, None, None]
    fill = top[None] * (1 - w) + bot[None] * w
    reg = o[Y0:Y1].copy(); reg[:, X0:X1] = fill[:, X0:X1]
    # bordas suaves nas laterais
    for k in range(6):
        al = (k + 1) / 7
        reg[:, X0 - 6 + k] = o[Y0:Y1, X0 - 6 + k] * (1 - al) + fill[:, X0 - 6 + k] * al
        reg[:, X1 + 5 - k] = o[Y0:Y1, X1 + 5 - k] * (1 - al) + fill[:, X1 + 5 - k] * al
    new = o.copy(); new[Y0:Y1] = reg
    tl = TL[:, None] if False else TL[..., None]
    new[40:140] = new[40:140] * (1 - tl) + COR * tl
    ba = BA; new[BY:BY + 24, BX - 12:BX + 12] = new[BY:BY + 24, BX - 12:BX + 12] * (1 - ba) + BADGE * ba
    out = o * (1 - a) + new * a
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)
if __name__ == "__main__":
    import sys
    f = REF.copy(); g = aplica(f)
    Image.fromarray(np.vstack([f[20:130, 150:470], g[20:130, 150:470]])).resize((960, 660), Image.LANCZOS).save(T / "arroba_teste.png")
    print("forca", forca(f), "badge x", BX)

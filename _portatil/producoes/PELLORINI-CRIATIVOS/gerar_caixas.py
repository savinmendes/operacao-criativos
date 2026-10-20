# -*- coding: utf-8 -*-
"""Família 'caixa nas mãos' (Pelvini 015/057) com as fotos de caixa já trocadas para PELLORINI."""
import os, glob
from PIL import Image, ImageDraw
import gerar_lote as g1
import gerar_lote2 as g2

ORIG = os.path.join(g1.BASE, "caixas_pellorini", "pellorini")
SAIDA = os.path.join(g1.BASE, "lote3-vencedores", "caixa-maos")
os.makedirs(SAIDA, exist_ok=True)
TIT = {"vittorio_2": "Unbox the Vittorio.", "pelvini-milano_2": "Unbox the Milano.", "pelvini-dominante_2": "Unbox the Dominante.",
       "pelvini-opulent_2": "Unbox the Opulent.", "pelvini-opulent_5": "Built to be noticed.", "pelvini-opulent_6": "Solid engineering.",
       "pelvini-maretti-1_2": "Unbox the Maretti.", "pelvini-maretti-1_6": "Quiet luxury, boxed."}

def caixa(fmt, arq, titulo):
    w, h = g1.FORMATOS[fmt]
    a = fmt == "9x16"
    im = g2.cobrir(Image.open(arq).convert("RGB"), w, h, 0.5)
    im = g2.degrade_baixo(im, 0.62, 235)
    topo = Image.new("RGB", (w, 190 if not a else 380), (0, 0, 0))
    msk = Image.linear_gradient("L").rotate(180).resize(topo.size).point(lambda v: int(v * 0.85))
    im.paste(topo, (0, 0), msk)
    d = ImageDraw.Draw(im)
    g1.texto_c(d, w, 50 if not a else 170, titulo, g1.fonte("serif", 74 if not a else 86, 600), g1.CREAM)
    y = h - (270 if not a else 520)
    bw = (w - 3 * 40) / 2
    for i, (t1, t2) in enumerate([("316L STEEL", "Built to last"), ("2-YEAR", "Warranty")]):
        x = 40 + i * (bw + 40)
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle((x, y, x + bw, y + 110), radius=14, fill=(8, 8, 8, 225), outline=g1.GOLD + (255,), width=2)
        im.paste(ov, (0, 0), ov)
        d = ImageDraw.Draw(im)
        g2.texto_c_x(d, x + bw / 2, y + 16, t1, g1.fonte("sans", 30, 800), g1.GOLD)
        g2.texto_c_x(d, x + bw / 2, y + 60, t2, g1.fonte("sans", 28, 500), g1.CREAM)
    g1.pilula(d, w / 2, y + 140, "BUY 1 GET 1 FREE", g1.fonte("sans", 32, 800), g1.GOLD, g1.INK)
    return im

n = 0
for arq in sorted(glob.glob(os.path.join(ORIG, "*.jpg"))):
    b = os.path.basename(arq)[:-4]
    for fmt in g1.FORMATOS:
        caixa(fmt, arq, TIT.get(b, "Unbox Pellorini.")).save(os.path.join(SAIDA, f"C7_P1_caixa-maos_{b}_{fmt}.jpg"), quality=92)
        n += 1
print(n, "imagens")
g2.folha(sorted(glob.glob(os.path.join(SAIDA, "*_1x1.jpg"))), os.path.join(SAIDA, "_revisao.jpg"), w=300, cols=4)

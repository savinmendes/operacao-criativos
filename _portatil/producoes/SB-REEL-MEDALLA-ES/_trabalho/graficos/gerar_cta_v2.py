# -*- coding: utf-8 -*-
"""v2: setas amarelas separadas do texto (ficam do 1º CTA até o fim) + 2 textos: «MÁS INFORMACIÓN» e «VER MÁS»."""
import gerar_graficos as g

def texto(partes, nome):
    im = g.tela(); d = g.ImageDraw.Draw(im)
    f = g.F("ExtraBold", 64)
    tot = sum(g.larg(d, t, f, 6)[0] for t, _ in partes)
    if tot > 1000:
        f = g.caber(d, "".join(t for t, _ in partes), "ExtraBold", 64, 1000, 6)
    tot = sum(d.textlength(t, font=f) for t, _ in partes)
    x = (g.W - tot) / 2; cy = 1572
    for t, c in partes:
        d.text((x, cy), t, font=f, fill=c, stroke_width=6, stroke_fill=g.ESCURO, anchor="lm")
        x += d.textlength(t, font=f)
    g.sombra(im, 8, 130, (0, 5)).save(g.AQUI / nome)

B = (255, 255, 255, 255)
texto([("TOCA ", B), ("«MÁS INFORMACIÓN»", g.AMARELO)], "cta_txt_masinfo.png")
texto([("TOCA ", B), ("«VER MÁS»", g.AMARELO), (" AQUÍ ABAJO", B)], "cta_txt_vermas.png")
im = g.tela(); s = g.seta(150, 176)
for cx in (385, 695):
    im.alpha_composite(s, (int(cx - 75), 1620))
g.sombra(im, 8, 130, (0, 5)).save(g.AQUI / "cta_setas.png")
print("ok")

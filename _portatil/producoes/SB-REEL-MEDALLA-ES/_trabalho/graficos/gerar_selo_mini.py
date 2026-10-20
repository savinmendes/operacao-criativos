# -*- coding: utf-8 -*-
"""Selo "VIDEO FICTICIO" pela metade (fonte 18, caixa proporcional), colado no topo (y=4) à direita."""
import gerar_graficos as g
im = g.tela(); d = g.ImageDraw.Draw(im)
f = g.F("Bold", 18); t = "VIDEO FICTICIO"
w, h, b = g.larg(d, t, f)
px, py = 11, 6
x1 = g.W - 20; x0 = x1 - w - 2 * px
y0 = 4; y1 = y0 + h + 2 * py
d.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=(0, 0, 0, 179))
d.text((x0 + px - b[0], y0 + py - b[1]), t, font=f, fill=(255, 255, 255, 255))
im.save(g.AQUI / "selo_ficticio_mini.png")
print("ok", (x0, y0, x1, y1))

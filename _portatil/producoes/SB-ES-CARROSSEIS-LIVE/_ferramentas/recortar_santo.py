# -*- coding: utf-8 -*-
"""Recorta figura sobre fundo preto puro -> PNG transparente, aparado ao conteudo.
Interior da silhueta fica opaco (habito escuro nao vaza); a borda usa alpha por luminancia com a cor
despremultiplicada, entao sobre fundo preto reproduz o original sem halo.
Uso: python recortar_santo.py entrada.png saida.png"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

a = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
m = a.max(axis=2)
lum_a = np.clip((m - 3.0) / 22.0, 0, 1)

# silhueta: pixels > 8, fechada, buracos preenchidos (flood fill do exterior)
sil = Image.fromarray(((m > 8) * 255).astype(np.uint8))
sil = sil.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
h, w = m.shape
borda = Image.new("L", (w + 2, h + 2), 0)
borda.paste(sil, (1, 1))
ImageDraw.floodfill(borda, (0, 0), 128)
ext = np.asarray(borda)[1:-1, 1:-1] == 128
interior = Image.fromarray((~ext * 255).astype(np.uint8))
# encolhe o interior para a borda continuar sendo decidida pela luminancia
interior = interior.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(2))
alpha = np.maximum(lum_a, np.asarray(interior).astype(np.float32) / 255.0)

rgb = np.where(alpha[..., None] > 0.01, np.clip(a / np.maximum(alpha[..., None], 1e-3), 0, 255), 0)
out = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
bb = Image.fromarray(((alpha > 0.03) * 255).astype(np.uint8)).getbbox()
out = out.crop(bb)
out.save(sys.argv[2])
# checagem: sobre preto deve reproduzir o original
comp = Image.new("RGB", out.size, (0, 0, 0)); comp.paste(out, (0, 0), out)
diff = np.abs(np.asarray(comp).astype(int) - a[bb[1]:bb[3], bb[0]:bb[2]].astype(int)).max()
print("bbox", bb, "size", out.size, "dif max sobre preto", diff)

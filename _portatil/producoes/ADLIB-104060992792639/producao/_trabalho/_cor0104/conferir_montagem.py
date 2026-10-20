# -*- coding: utf-8 -*-
"""Confere que a montagem nova reproduz a anterior (mesma boca, mesmas emendas): base_lipsync nova x _antes_cor/base_lipsync,
na regiao da boca, a cada 3 quadros, depois de tirar a diferenca de cor (afim por quadro). Imprime a dif. media de estrutura
(nivel de recodificacao ~1-2) e os piores quadros. Uso: python conferir_montagem.py NN x y w h"""
import sys, numpy as np
from util import T, quadros, ajustar, aplicar
NN = sys.argv[1]; x, y, w, h = map(int, sys.argv[2:6]); AD = T / f"ad{NN}"
ds = []
for i, (a, b) in enumerate(zip(quadros(AD / "base_lipsync.mp4"), quadros(AD / "_antes_cor" / "base_lipsync.mp4"))):
    if i % 3: continue
    A_, B_ = a[y:y + h, x:x + w], b[y:y + h, x:x + w]
    M, *_ = ajustar(B_[::2, ::2], A_[::2, ::2], it=2)
    ds.append((float(np.abs(aplicar(M, B_).astype(float) - A_).mean()), i))
d = np.array([v for v, _ in ds]); print(f"AD {NN}: {len(d)} quadros, dif. estrutura boca media {d.mean():.2f} mediana {np.median(d):.2f} p99 {np.percentile(d, 99):.2f}")
print("piores:", sorted(ds, reverse=True)[:6])

# -*- coding: utf-8 -*-
"""Diagnostico: diferenca media de cada retangulo de mascara entre cada quadro e o quadro de referencia (still).
Uso: python ov_diag.py ov.json"""
import sys, json, numpy as np
from comum3 import quadros
cfg = json.load(open(sys.argv[1]))
S = next(quadros(cfg["video"], cfg["still"], 1)).astype(np.float32)
q0, q1 = cfg["janela"]
for k, f in enumerate(quadros(cfg["video"], q0, q1 - q0)):
    f = f.astype(np.float32); q = q0 + k
    ds = [np.abs(f[y0:y1, x0:x1] - S[y0:y1, x0:x1]).mean() for x0, y0, x1, y1 in cfg["lama"] + cfg["fundo"]]
    print(q, " ".join(f"{d:5.1f}" for d in ds))

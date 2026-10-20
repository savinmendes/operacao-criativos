# -*- coding: utf-8 -*-
"""Confere que a base_lipsync nova reproduz a montagem anterior (mesma geometria/camadas), ignorando a cor:
por quadro, afim BGR robusta nova -> antiga (_antes_cor) e residuo em blocos de 16x16. Quadro com bloco > LIM = suspeito.
Uso: python verificar.py [arq_novo] [arq_antigo]"""
import sys
from pathlib import Path
import numpy as np, cv2
C = Path(__file__).resolve().parent; AD = C.parent
sys.path.insert(0, str(AD.parent / "ad13" / "lipsync3"))
from comum3 import quadros
nv = Path(sys.argv[1]) if len(sys.argv) > 1 else AD / "base_lipsync.mp4"
av = Path(sys.argv[2]) if len(sys.argv) > 2 else AD / "_antes_cor" / "base_lipsync.mp4"
LIM = 14
def ajustar(X, Y):
    X = X.astype(np.float64); Y = Y.astype(np.float64); Xa = np.c_[X, np.ones(len(X))]; ok = np.ones(len(X), bool)
    for _ in range(3):
        A, *_ = np.linalg.lstsq(Xa[ok], Y[ok], rcond=None); r = np.linalg.norm(Xa @ A - Y, axis=1); ok = r < max(3, 2.5 * np.median(r[ok]))
    return A
res = []; ruins = []
for q, (a, b) in enumerate(zip(quadros(nv), quadros(av))):
    A = ajustar(a[::4, ::4].reshape(-1, 3), b[::4, ::4].reshape(-1, 3))
    p = (a.reshape(-1, 3).astype(np.float32) @ A[:3].astype(np.float32) + A[3].astype(np.float32)).reshape(a.shape)
    d = np.abs(p - b).mean(-1)
    blk = cv2.resize(d, (45, 80), interpolation=cv2.INTER_AREA)
    res.append((q, d.mean(), blk.max()))
    if blk.max() > LIM:
        y, x = np.unravel_index(blk.argmax(), blk.shape); ruins.append((q, round(float(blk.max()), 1), (x * 16, y * 16)))
r = np.array(res)
print(f"{len(r)} quadros | residuo medio {r[:,1].mean():.2f} (max {r[:,1].max():.2f} em q{int(r[r[:,1].argmax(),0])}) | pior bloco 16x16: mediana {np.median(r[:,2]):.1f}, max {r[:,2].max():.1f}")
for a0, a1, nm in [(0, 75, "c1"), (75, 87, "plano"), (87, 161, "cobertos m1/cl"), (161, 196, "plano"), (196, 286, "coberto mz"), (286, 653, "c2-c3"),
                   (653, 1271, "m3-m5 v3"), (1271, 1302, "plano"), (1302, 1712, "d1-d2 v3"), (1712, 2298, "d3-d5")]:
    s = r[a0:a1]; print(f"  {nm:16} q{a0}-{a1-1}: residuo medio {s[:,1].mean():.2f} | pior bloco mediana {np.median(s[:,2]):.1f} max {s[:,2].max():.1f} (q{int(s[s[:,2].argmax(),0])})")
print("quadros com bloco >", LIM, ":", len(ruins), ruins[:40])

# -*- coding: utf-8 -*-
"""QA do take: folha da boca quadro a quadro (cada 2 quadros) + folha geral + luma. Uso: python qa.py take.mp4 tag"""
import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
from pathlib import Path
AQ = Path(__file__).resolve().parent; tk, tag = sys.argv[1], sys.argv[2]
F = list(quadros(tk)); print(len(F), "quadros")
boca = [cv2.resize(f[760:940, 40:300], (195, 135)) for f in F[::2]]
while len(boca) % 7: boca.append(np.zeros_like(boca[0]))
rows = [np.hstack(boca[i:i + 7]) for i in range(0, len(boca), 7)]
cv2.imwrite(str(AQ / "w" / f"qa_boca_{tag}.jpg"), np.vstack(rows))
g = [cv2.resize(f[450:1240, 0:420], (210, 395)) for f in F[::12]]
cv2.imwrite(str(AQ / "w" / f"qa_geral_{tag}.jpg"), np.hstack(g))

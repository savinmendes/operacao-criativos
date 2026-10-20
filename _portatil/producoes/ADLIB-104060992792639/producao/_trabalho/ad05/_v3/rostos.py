# -*- coding: utf-8 -*-
"""Rostos (MediaPipe) e cortes de câmera na base_sem_legenda_lama.mp4 (24 fps, tempo novo) nos trechos do v3."""
import sys, os, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
from pathlib import Path
AD = Path(__file__).resolve().parent.parent
cap = cv2.VideoCapture(str(AD/"base_sem_legenda_lama.mp4"))
fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
print("N", len(fr))
for i in range(1, len(fr)):
    d = np.abs(cv2.resize(fr[i],(90,160)).astype(np.float32)-cv2.resize(fr[i-1],(90,160)).astype(np.float32)).mean()
    if d > 15: print(f"corte q{i} ({i/24:.2f}s) d={d:.1f}")
R = cl.Rastreador(multi=True)
def nms(bx):
    bx = sorted(bx, key=lambda b: -b[2]*b[3]); out = []
    for b in bx:
        cx, cy = b[0]+b[2]/2, b[1]+b[3]/2
        if all(not (o[0] <= cx <= o[0]+o[2] and o[1] <= cy <= o[1]+o[3]) for o in out): out.append(b)
    return out
for q in [90, 100, 115, 660, 760, 880, 900, 1000, 1130, 1140, 1260, 1305, 1400, 1470, 1500, 1600, 1700]:
    print(q, f"{q/24:.2f}s", nms(R.todos_rostos(fr[q])))
    cv2.imwrite(f"q{q}.jpg", cv2.resize(fr[q], (360, 640)))

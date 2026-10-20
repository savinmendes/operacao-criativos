# -*- coding: utf-8 -*-
"""Correcao de cor: refaz SO a parte de geometria do _loteA/fechar_c1.py (marcos, pausas e quadro de referencia),
lendo a MESMA entrada daquela rodada (_antes_loteA/base_lipsync.mp4, cv2) para que a colagem em memoria seja identica.
Saida: c1_marcos.npz (P 75x478x2, ab, runs, r). Nada de video e gravado."""
import sys, os
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
AD = Path(__file__).resolve().parent.parent; FPS = 24; A, B = 0, 75; MINQ = 5
cap = cv2.VideoCapture(str(AD / "_antes_loteA/base_lipsync.mp4")); NT = int(cap.get(7)); fr = []
for q in range(B):
    ok, f = cap.read(); fr.append(f)
R = cl.Rastreador(alvo=(380, 0, 300, 320))
P = [R.pontos(fr[q]) for q in range(A, B)]
ab = np.array([cl._abertura(p) if p is not None else np.nan for p in P]); n = B - A
es = cl.envelope(cl.ler_audio(AD / "narr_clara.wav"), 16000, float(FPS), NT)[A:B]
fal = es > np.nanmax(es) - 30
runs, k = [], 0
while k < n:
    if not fal[k]:
        j = k
        while j < n and not fal[j]: j += 1
        if j - k >= MINQ and k > 0: runs.append((k, j))
        k = j
    else: k += 1
viz = [q for q in range(n) if np.isfinite(ab[q]) and fal[q]]; r = min(viz, key=lambda q: ab[q])
PP = np.array([p if p is not None else np.full((478, 2), np.nan) for p in P])
np.savez(Path(__file__).parent / "c1_marcos.npz", P=PP, ab=ab, runs=np.array(runs), r=r, NT=NT)
print("NT", NT, "runs", runs, "ref", r, "ab", round(float(ab[r]), 3), "sem marcos", int(np.isnan(PP[:, 0, 0]).sum()))

# -*- coding: utf-8 -*-
"""Índice de pausa (checar_lipsync) só nas janelas em que o avatar aparece na montagem.
Uso: python indice_visivel.py video.mp4 audio.mp3 "a-b,c-d" (s locais do clipe)"""
import sys
from pathlib import Path
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
sys.path.insert(0, str(KIT))
v, a, jan = sys.argv[1:4]
sys.argv = [sys.argv[0]]
import numpy as np  # noqa: E402
import checar_lipsync as CL  # noqa: E402

fps, ab, *_ = CL.series_video(Path(v), None)
env = CL.envelope(CL.ler_audio(a), 16000, fps, len(ab))
fala = CL.mascara_fala(env)
pausa = CL.mascara_pausas(fala)
vis = np.zeros(len(ab), bool)
for j in jan.split(","):
    x, y = map(float, j.split("-"))
    vis[int(x * fps):int(y * fps)] = True
ok = np.isfinite(ab)
p, f = pausa & vis & ok, fala & vis & ok
print(f"{Path(v).name}: indice visivel {np.mean(ab[p]) / np.mean(ab[f]):.2f} ({p.sum()} q pausa) | total {np.mean(ab[pausa & ok]) / np.mean(ab[fala & ok]):.2f}")

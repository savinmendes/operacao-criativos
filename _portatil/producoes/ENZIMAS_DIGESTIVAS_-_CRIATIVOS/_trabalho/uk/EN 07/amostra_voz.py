# -*- coding: utf-8 -*-
"""Junta os trechos da voz isolada (demucs) em que so a creator da esquerda fala -> amostra_voz_mulher.wav
Uso: python amostra_voz.py "a-b,c-d,..." """
import sys, numpy as np, soundfile as sf
x, sr = sf.read("demucs/htdemucs/orig/vocals.wav")
gap = np.zeros((int(0.25 * sr), x.shape[1]))
parts = []
for p in sys.argv[1].split(","):
    a, b = map(float, p.split("-")); parts += [x[int(max(0, a - 0.05) * sr):int((b + 0.08) * sr)], gap]
y = np.concatenate(parts); sf.write("amostra_voz_mulher.wav", y, sr); print(round(len(y) / sr, 1), "s")

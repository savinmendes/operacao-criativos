# -*- coding: utf-8 -*-
"""Áudios para o HeyGen (Avatar IV): mulher M = M3..M5; Juan A = J06..J09, B = J10..J13.
Cada fala é cortada na extensão da voz e separada por GAP; 0,25 s antes e 0,40 s depois.
Grava <dir>/<nome>.wav/.mp3 e avatares.json com as palavras no tempo de cada vídeo de avatar."""
import json, subprocess, numpy as np, soundfile as sf, librosa
from pathlib import Path
from pal import pal
P = Path(__file__).resolve().parent; TT = P / "tts"; SR = 44100; PRE, POS, GAP = 0.25, 0.40, 0.35
def extensao(y):
    db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0] + 1e-9); on = np.where(db > -40)[0]
    return max(0, on[0] * 256 / SR - 0.03), min(len(y) / SR, on[-1] * 256 / SR + 1024 / SR + 0.06)
GR = {"M": ("mulher", ["M3", "M4", "M5"]), "A": ("avatar", ["J06", "J07", "J08", "J09"]), "B": ("avatar", ["J10", "J11", "J12", "J13"])}
meta = {}
for nome, (d, ks) in GR.items():
    partes = [np.zeros(int(PRE * SR))]; t = PRE; pals = []; lin = []
    for i, k in enumerate(ks):
        y, _ = librosa.load(TT / f"{k}.mp3", sr=SR); a, b = extensao(y); s = y[int(a * SR):int(b * SR)].copy()
        n = int(.008 * SR); s[:n] *= np.linspace(0, 1, n); s[-n:] *= np.linspace(1, 0, n)
        for w, x, z in pal(TT / f"{k}.alinhamento.json"):
            if x >= a - 0.25 and x < b: pals.append(dict(w=w, ini=round(max(x, a) - a + t, 3), fim=round(min(z, b) - a + t, 3), linha=k))
        lin.append(dict(k=k, ini=round(t, 3), fim=round(t + len(s) / SR, 3)))
        partes.append(s); t += len(s) / SR
        if i < len(ks) - 1: partes.append(np.zeros(int(GAP * SR))); t += GAP
    partes.append(np.zeros(int(POS * SR)))
    V = np.concatenate(partes); f = P / d / f"{nome}.wav"; sf.write(f, V, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-b:a", "192k", str(f.with_suffix(".mp3"))], check=True)
    meta[nome] = dict(arquivo=str(f.with_suffix(".mp3").relative_to(P)), dur=round(len(V) / SR, 3), linhas=lin, palavras=pals)
    print(nome, round(len(V) / SR, 2), [(l["k"], l["ini"], l["fim"]) for l in lin])
json.dump(meta, open(P / "avatares.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

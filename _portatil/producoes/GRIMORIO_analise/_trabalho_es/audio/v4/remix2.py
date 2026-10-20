# -*- coding: utf-8 -*-
"""v4 (sobre o áudio do FINAL): tira a voz antiga do grito (demucs do trecho), põe a tomada nova e o ambiente de igreja 0:00-0:08.
Do 0:08,05 em diante o áudio fica idêntico ao final. uso: python remix2.py <grito.mp3> <amb.mp3> <video_in> <video_out> [estica 0/1]"""
import sys, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
W = Path(__file__).resolve().parent; SR = 44100
g_arq, amb_arq, vin, vout = sys.argv[1:5]; estica = len(sys.argv) > 5 and sys.argv[5] == "1"
med = pyln.Meter(SR)
def ld(p): return librosa.load(p, sr=SR, mono=True)[0]
def fx(y, f):
    sf.write(W / "_in.wav", y, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "_in.wav"), "-af", f, "-c:a", "pcm_f32le", str(W / "_out.wav")], check=True)
    return sf.read(W / "_out.wav")[0]
def fade(y, a=0.01, b=0.04):
    y = y.copy(); na, nb = int(a * SR), int(b * SR); y[:na] *= np.linspace(0, 1, na); y[-nb:] *= np.linspace(1, 0, nb); return y
orig = sf.read(W / "final_estereo.wav")[0]                      # (n, 2)
voc = sf.read(W / "sep/htdemucs/ini10/vocals.wav")[0]           # (10 s, 2)
T0, R0, R1 = 4.10, 4.38, 7.75
a, b = int(R0 * SR), int(R1 * SR); c = int(0.03 * SR)
w = np.ones(b - a); w[:c] = np.linspace(0, 1, c); w[-c:] = np.linspace(1, 0, c)
lo_old = med.integrated_loudness(voc[a:b])
out = orig.copy(); out[a:b] -= voc[a:b] * w[:, None]           # sai a voz antiga do grito, a música fica
g = ld(g_arq)
ws = [(0.0, 0.62), (0.80, 3.05)]; alvo = [(0.37, 1.04), (1.06, 3.48)]
novo = np.zeros(int(3.7 * SR))
for (s0, s1), (t0, t1) in zip(ws, alvo):
    seg = g[int(s0 * SR): int(s1 * SR)]
    if estica:
        r = (len(seg) / SR) / (t1 - t0 + 0.12)
        if abs(r - 1) > 0.03: seg = librosa.effects.time_stretch(seg, rate=r)
    seg = fade(seg); n = int(t0 * SR); novo[n: n + len(seg)] += seg[: len(novo) - n]
novo = fx(novo, "highpass=f=110,aecho=0.85:0.5:40|85:0.16|0.09")
novo = novo * 10 ** ((lo_old + 1.0 - med.integrated_loudness(novo)) / 20)
n = int(T0 * SR); out[n: n + len(novo)] += novo[:, None]
amb = fx(ld(amb_arq), "highpass=f=80,aecho=0.8:0.5:70:0.2")[: int(8.05 * SR)]
env = np.ones(len(amb)); fi, fo = int(0.25 * SR), int(7.45 * SR); env[:fi] = np.linspace(0, 1, fi); env[fo:] = np.linspace(1, 0, len(env) - fo)
gl = np.full(len(amb), 10 ** (-27 / 20)); gl[int(4.35 * SR): int(7.6 * SR)] = 10 ** (-24 / 20)
k = int(0.2 * SR); gl = np.convolve(gl, np.ones(k) / k, mode="same")
amb = amb / 10 ** (med.integrated_loudness(amb) / 20) * gl * env
out[: len(amb)] += amb[:, None]
pk = np.abs(out[: int(8.1 * SR)]).max()
# limitador sem atraso só em 0-8,6 s (o resto do áudio não é tocado): ganho = 0,84/pico na janela de 10 ms, suavizado
from scipy.ndimage import maximum_filter1d, uniform_filter1d
seg = out[: int(8.6 * SR)]; env = maximum_filter1d(np.abs(seg).max(1), size=int(0.010 * SR))
gan = np.minimum(1.0, 0.84 / np.maximum(env, 1e-9)); gan = np.minimum(gan, uniform_filter1d(gan, int(0.005 * SR)))
out[: int(8.6 * SR)] = seg * gan[:, None]
sf.write(W / "mix_v4.wav", out, SR, subtype="PCM_16")
sf.write(W / "grito_novo_so_voz.wav", novo, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vin, "-i", str(W / "mix_v4.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-ar", "44100", "-shortest", "-movflags", "+faststart", vout], check=True)
print("ok | LUFS voz antiga", round(lo_old, 1), "| pico 0-8s", round(float(pk), 3))

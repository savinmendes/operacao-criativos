# -*- coding: utf-8 -*-
"""Trilha propria (sintese local, sem direitos de terceiros) + efeitos de borrifada.
  python trilha_lux.py lux 40 audio/trilha_lux.wav      -> instrumental escuro/luxo, 92 BPM, Dm, kick + hat + pad + pluck
  python trilha_lux.py leve 40 audio/trilha_leve.wav    -> groove leve e alegre (esquete), 104 BPM, F maior
  python trilha_lux.py spray 0 audio/spray.wav          -> 'psssh' de borrifador (ruido filtrado)
Saida normalizada: lux/leve em -16 LUFS (a montagem ajusta o nivel), spray em pico -3 dBFS.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
MODO, DUR, SAIDA = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3])
SAIDA.parent.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def norm_ffmpeg(x, af):
    raw = SAIDA.with_suffix(".tmp.wav")
    sf.write(raw, x.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(SAIDA)], check=True)
    raw.unlink()


if MODO == "spray":
    n = int(0.75 * SR)
    t = np.arange(n) / SR
    ru = rng.standard_normal(n)
    env = np.where(t < 0.02, t / 0.02, np.exp(-(t - 0.02) * 4.0))
    clique = np.zeros(n)
    k = int(0.004 * SR)
    clique[:k] = np.hanning(2 * k)[:k] * 0.6
    x = ru * env * 0.5 + clique
    x = np.stack([x, x], 1)
    norm_ffmpeg(x, "highpass=f=2500,lowpass=f=11000,aecho=0.6:0.4:25:0.25,volume=1.0,alimiter=limit=0.7")
    print("ok", SAIDA)
    sys.exit()

n = int(DUR * SR)
t = np.arange(n) / SR
L = np.zeros(n, np.float32)
R = np.zeros(n, np.float32)
lux = MODO == "lux"
bpm = 92 if lux else 104
beat = 60 / bpm
acordes = ([[38, 50, 53, 57, 62], [34, 46, 50, 53, 58], [36, 48, 52, 55, 60], [33, 45, 49, 52, 57]] if lux else
           [[41, 53, 57, 60, 65], [38, 50, 53, 57, 62], [34, 46, 50, 53, 58], [36, 48, 52, 55, 60]])
bar = 4 * beat


def add(i0, sig, pan=0.5):
    i1 = min(n, i0 + len(sig))
    if i0 >= n:
        return
    L[i0:i1] += sig[:i1 - i0] * (1 - pan)
    R[i0:i1] += sig[:i1 - i0] * pan


# pad (acorde por compasso)
k = 0
a = 0.0
while a < DUR:
    notas = acordes[k % 4]
    m = int((bar + 1.0) * SR)
    tt = np.arange(m) / SR
    env = np.clip(np.minimum(tt / 0.8, (bar + 1.0 - tt) / 0.8), 0, 1)
    for j, nt in enumerate(notas):
        for det, pan in ((-0.6, 0.25), (0.6, 0.75)):
            s = np.sin(2 * np.pi * (hz(nt) + det) * tt) + 0.2 * np.sin(2 * np.pi * 2 * (hz(nt) + det) * tt)
            add(int(a * SR), (0.05 * (1.5 if j == 0 else 1) * env * s).astype(np.float32), pan)
    # baixo
    sb = np.sin(2 * np.pi * hz(notas[0] - 12 if lux else notas[0]) * tt) * np.exp(-tt * 1.2)
    add(int(a * SR), (0.22 * sb * np.clip(tt / 0.01, 0, 1)).astype(np.float32))
    # pluck em colcheias
    for q in range(8):
        ts = a + q * beat / 2
        nt = notas[1:][(q * 3) % 4] + 12
        mm = int(0.8 * SR)
        t2 = np.arange(mm) / SR
        sp = np.exp(-t2 * (7 if lux else 9)) * (np.sin(2 * np.pi * hz(nt) * t2) + 0.4 * np.sin(2 * np.pi * 2 * hz(nt) * t2))
        add(int(ts * SR), (0.035 * sp).astype(np.float32), 0.3 if q % 2 else 0.7)
    a += bar
    k += 1

# bateria
nb = int(DUR / beat) + 1
for b in range(nb):
    ts = b * beat
    i0 = int(ts * SR)
    mm = int(0.35 * SR)
    t2 = np.arange(mm) / SR
    if b % 2 == 0 or not lux:   # kick
        f = 50 + 90 * np.exp(-t2 * 30)
        kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 * 9)
        add(i0, (0.55 * kick).astype(np.float32))
    if b % 2 == 1:   # clap/snare suave
        sn = rng.standard_normal(mm) * np.exp(-t2 * 22)
        add(i0, (0.12 * sn).astype(np.float32))
    for h in (0, 0.5):   # hat
        hh = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90)
        add(int((ts + h * beat) * SR), (0.05 * hh).astype(np.float32), 0.6)

x = np.stack([L, R], 1)
x /= np.abs(x).max() + 1e-9
x *= 0.7
fi, fo = int(0.2 * SR), int(1.2 * SR)
x[:fi] *= np.linspace(0, 1, fi)[:, None]
x[-fo:] *= np.linspace(1, 0, fo)[:, None]
filtro = ("highpass=f=30,lowpass=f=9000,aecho=0.8:0.5:110|220:0.25|0.12" if lux else
          "highpass=f=35,lowpass=f=10000,aecho=0.8:0.5:90:0.18")
norm_ffmpeg(x, filtro + ",loudnorm=I=-16:TP=-2:LRA=9")
print("ok", SAIDA)

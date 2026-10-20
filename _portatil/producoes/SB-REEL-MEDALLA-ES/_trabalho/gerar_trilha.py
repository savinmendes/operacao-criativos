# -*- coding: utf-8 -*-
"""Trilha própria (sintetizada aqui, sem direitos de terceiros): pad suave de oração em Ré maior.
Acordes lentos D - Bm - G - A (8 s cada) com parciais senoidais levemente desafinadas, ataque/soltura longos,
um "sino" suave a cada troca de acorde. Saída: audio/trilha.wav (48 kHz estéreo), duração = argv[1] s.
Rodar em _trabalho:  python gerar_trilha.py 121.5
"""
import sys, subprocess
import numpy as np
from pathlib import Path

SR = 48000
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 122.0
OUT = Path(__file__).resolve().parent / "audio"
OUT.mkdir(exist_ok=True)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# acordes (MIDI): baixo + tríade aberta
ACORDES = [
    [38, 50, 57, 62, 66],   # D
    [35, 47, 54, 59, 62],   # Bm
    [31, 43, 50, 55, 59],   # G
    [33, 45, 52, 57, 61],   # A
]
CH = 8.0
n = int(DUR * SR)
t = np.arange(n) / SR
L = np.zeros(n, np.float32)
R = np.zeros(n, np.float32)
rng = np.random.default_rng(7)
k = 0
start = 0.0
while start < DUR:
    notas = ACORDES[k % 4]
    a = int(max(0, start - 2.0) * SR)
    b = int(min(DUR, start + CH + 2.0) * SR)
    tt = t[a:b] - (start - 2.0)
    seg_len = (b - a) / SR
    env = np.clip(np.minimum(tt / 3.0, (seg_len - tt) / 3.0), 0, 1) ** 1.5
    for j, m in enumerate(notas):
        f = hz(m)
        amp = 0.16 if j == 0 else 0.09
        for det, pan in ((-0.6, 0.3), (0.6, 0.7)):
            ph = rng.uniform(0, 2 * np.pi)
            s = np.sin(2 * np.pi * (f + det) * tt + ph) + 0.25 * np.sin(2 * np.pi * 2 * (f + det) * tt + ph)
            v = (amp * env * s).astype(np.float32)
            L[a:b] += v * (1 - pan)
            R[a:b] += v * pan
    # sino suave na troca
    sa = int(start * SR)
    sb = min(n, sa + int(5 * SR))
    ts = t[sa:sb] - start
    fb = hz(notas[-1] + 12)
    bell = (0.05 * np.exp(-ts * 0.9) * (np.sin(2 * np.pi * fb * ts) + 0.4 * np.sin(2 * np.pi * fb * 2.76 * ts))).astype(np.float32)
    L[sa:sb] += bell * 0.6
    R[sa:sb] += bell * 0.4
    start += CH
    k += 1

x = np.stack([L, R], 1)
x /= np.abs(x).max() + 1e-9
x *= 0.7
fade = int(2.0 * SR)
x[:fade] *= np.linspace(0, 1, fade)[:, None]
x[-fade:] *= np.linspace(1, 0, fade)[:, None]
raw = OUT / "_trilha_seca.f32"
raw.write_bytes(x.astype(np.float32).tobytes())
# reverb leve + passa-baixa, e normaliza em -32 LUFS
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw),
                "-af", "aecho=0.8:0.6:90|170|260:0.35|0.25|0.15,lowpass=f=5000,loudnorm=I=-32:TP=-6:LRA=7",
                "-ar", str(SR), str(OUT / "trilha.wav")], check=True)
raw.unlink()
print("ok", OUT / "trilha.wav")

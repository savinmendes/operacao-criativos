# -*- coding: utf-8 -*-
"""Trilhas próprias em 2 climas (síntese local, sem direitos de terceiros).
  tensao     : grave e escura. Drone de Ré + acordes menores lentos (Dm - Bb - Gm - A), pulso grave lento,
               passa-baixa forte e sem sino.
  esperanca  : clara e maior, registro mais alto (D - A - Bm - G, 6 s cada), arpejo suave tipo celesta e
               subida de volume de 0 a +4 dB ao longo da faixa.
Uso: python gerar_trilha2.py tensao 12 audio/trilha_tensao.wav
     python gerar_trilha2.py esperanca 52 audio/trilha_esperanca.wav
Saída normalizada em -32 LUFS (a montagem só soma sob a voz).
"""
import sys, subprocess
from pathlib import Path
import numpy as np

SR = 48000
MODO, DUR, SAIDA = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3])
n = int(DUR * SR); t = np.arange(n) / SR
rng = np.random.default_rng(11)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pad(notas, a, b, amp, brilho=0.25):
    """acorde com envelope longo entre a e b (s), devolve (L, R)."""
    i0, i1 = int(max(0, a - 1.5) * SR), int(min(DUR, b + 1.5) * SR)
    tt = t[i0:i1] - max(0, a - 1.5); L = tt[-1] if len(tt) else 1
    env = np.clip(np.minimum(tt / 2.0, (L - tt) / 2.0), 0, 1) ** 1.5
    l = np.zeros(i1 - i0, np.float32); r = np.zeros(i1 - i0, np.float32)
    for j, m in enumerate(notas):
        f = hz(m); am = amp * (1.6 if j == 0 else 1.0)
        for det, pan in ((-0.5, 0.3), (0.5, 0.7)):
            ph = rng.uniform(0, 2 * np.pi)
            s = np.sin(2 * np.pi * (f + det) * tt + ph) + brilho * np.sin(2 * np.pi * 2 * (f + det) * tt + ph)
            v = (am * env * s).astype(np.float32)
            l += v * (1 - pan); r += v * pan
    return i0, i1, l, r


L = np.zeros(n, np.float32); R = np.zeros(n, np.float32)
if MODO == "tensao":
    # drone grave de Ré com batimento lento
    drone = 0.20 * (np.sin(2 * np.pi * hz(26) * t) + 0.6 * np.sin(2 * np.pi * (hz(38) + 0.3) * t))
    drone *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t)     # pulso lento (respiração)
    L += drone.astype(np.float32); R += drone.astype(np.float32)
    acordes = [[38, 50, 53, 57], [34, 46, 50, 53], [31, 43, 46, 50], [33, 45, 49, 52]]  # Dm Bb Gm A
    ch = 4.0; k = 0; a = 0.0
    while a < DUR:
        i0, i1, l, r = pad(acordes[k % 4], a, a + ch, 0.07, brilho=0.1)
        L[i0:i1] += l; R[i0:i1] += r; a += ch; k += 1
    filtro = "lowpass=f=900,aecho=0.8:0.6:120|240:0.35|0.2"
    alvo_env = None
else:
    acordes = [[50, 62, 66, 69, 74], [45, 57, 61, 64, 69], [47, 59, 62, 66, 71], [43, 55, 59, 62, 67]]  # D A Bm G
    ch = 6.0; k = 0; a = 0.0
    while a < DUR:
        notas = acordes[k % 4]
        i0, i1, l, r = pad(notas, a, a + ch, 0.06, brilho=0.35)
        L[i0:i1] += l; R[i0:i1] += r
        # arpejo suave (celesta) 2 notas por segundo dentro do acorde
        for q in range(int(ch * 2)):
            ts = a + q * 0.5
            if ts >= DUR: break
            m = notas[1:][q % 4] + 12
            s0 = int(ts * SR); s1 = min(n, s0 + int(2.0 * SR)); tt = t[s0:s1] - ts
            b = (0.035 * np.exp(-tt * 2.2) * (np.sin(2 * np.pi * hz(m) * tt) + 0.3 * np.sin(2 * np.pi * hz(m) * 3 * tt))).astype(np.float32)
            pan = 0.35 if q % 2 else 0.65
            L[s0:s1] += b * (1 - pan); R[s0:s1] += b * pan
        a += ch; k += 1
    filtro = "highpass=f=90,lowpass=f=7000,aecho=0.8:0.6:90|180|270:0.3|0.2|0.12"
    alvo_env = True

x = np.stack([L, R], 1)
x /= np.abs(x).max() + 1e-9; x *= 0.7
fi = int(0.3 * SR); fo = int(1.5 * SR)
x[:fi] *= np.linspace(0, 1, fi)[:, None]; x[-fo:] *= np.linspace(1, 0, fo)[:, None]
raw = SAIDA.with_suffix(".f32"); raw.write_bytes(x.astype(np.float32).tobytes())
af = filtro + ",loudnorm=I=-32:TP=-6:LRA=7"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-af", af,
                "-ar", str(SR), str(SAIDA)], check=True)
raw.unlink()
if alvo_env:   # subida suave pós-normalização (0 -> +4 dB) mantendo média ~-32
    import soundfile as sf
    y, _ = sf.read(SAIDA, dtype="float32")
    g = 10 ** ((-2 + 4 * np.linspace(0, 1, len(y))) / 20)
    sf.write(SAIDA, (y * g[:, None]).astype(np.float32), SR)
print("ok", SAIDA)

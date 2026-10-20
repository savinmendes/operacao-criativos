# -*- coding: utf-8 -*-
"""v4: troca o grito (0:04-0:08) pela tomada eleven_v3 + ambiente de igreja em tumulto 0:00-0:08. Não regera o vídeo.
uso: python remix.py <grito.mp3> <ambiente.mp3> <video_entrada.mp4> <saida.mp4>"""
import sys, subprocess, numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from pathlib import Path
AQ = Path(__file__).resolve().parents[1]; W = Path(__file__).resolve().parent; SR = 44100
g_arq, amb_arq, vin, vout = sys.argv[1:5]
def ld(p): return librosa.load(p, sr=SR, mono=True)[0]
def fx(y, filtro):
    sf.write(W / "_in.wav", y, SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "_in.wav"), "-af", filtro, "-c:a", "pcm_f32le", str(W / "_out.wav")], check=True)
    return sf.read(W / "_out.wav")[0]
def fade(y, a=0.01, b=0.04):
    na, nb = int(a * SR), int(b * SR); y = y.copy(); y[:na] *= np.linspace(0, 1, na); y[-nb:] *= np.linspace(1, 0, nb); return y
med = pyln.Meter(SR)
voz = sf.read(AQ / "_tmp/voz_bruta.wav")[0]; mixb = sf.read(AQ / "_tmp/mix_bruto.wav")[0].T
mus = mixb - voz[None, :]                       # música = mix bruto - voz bruta (os dois antes do limitador)
T0 = 4.10                                        # início do take do grito no vídeo (quadro 123)
a, b = int((T0 + 0.28) * SR), int(7.75 * SR)
old = voz[a:b].copy(); lo_old = med.integrated_loudness(old)
voz[a:b] = 0
g = ld(g_arq)
ws = [(0.0, 0.62), (0.80, 3.05)]                 # "¡Graben!" | "¡No quieren que el pueblo prospere!" (tempos da tomada)
alvo = [(0.37, 1.04), (1.06, 3.48)]              # tempos da boca no take do Seedance (mesmos da v3)
novo = np.zeros(int(3.7 * SR))
for (s0, s1), (t0, t1) in zip(ws, alvo):
    seg = g[int(s0 * SR): int(s1 * SR)]
    r = (len(seg) / SR) / (t1 - t0 + 0.12)
    seg = fade(librosa.effects.time_stretch(seg, rate=r) if abs(r - 1) > 0.03 else seg)
    n = int(t0 * SR); novo[n: n + len(seg)] += seg[: len(novo) - n]
novo = fx(novo, "highpass=f=120,aecho=0.8:0.55:45|95:0.22|0.12")   # sala de igreja, gravado no celular
novo = novo * 10 ** ((lo_old - med.integrated_loudness(novo)) / 20)
n = int(T0 * SR); voz[n: n + len(novo)] += novo[: len(voz) - n]
amb = fx(ld(amb_arq), "highpass=f=80,aecho=0.8:0.5:70:0.2")
amb = amb[: int(8.05 * SR)]
env = np.ones(len(amb)); fi, fo0 = int(0.25 * SR), int(7.45 * SR)
env[:fi] = np.linspace(0, 1, fi); env[fo0:] = np.linspace(1, 0, len(env) - fo0)
gl = np.full(len(amb), 10 ** (-27 / 20)); gl[int(4.35 * SR): int(7.6 * SR)] = 10 ** (-24 / 20)   # mais alto no grito
gl = np.convolve(gl, np.ones(int(0.2 * SR)) / int(0.2 * SR), mode="same")
amb = amb / (10 ** (med.integrated_loudness(amb) / 20)) * gl * env
mix = mus.copy(); mix[:, : len(amb)] += amb[None, :]
sf.write(W / "_voz.wav", voz, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "_voz.wav"), "-af", "volume=0.7dB,alimiter=limit=0.80:attack=3:release=60:level=disabled", "-c:a", "pcm_f32le", str(W / "_voz_lim.wav")], check=True)
vl = sf.read(W / "_voz_lim.wav")[0][: mix.shape[1]]
mix[:, : len(vl)] += vl[None, :]
sf.write(W / "_mix.wav", mix.T, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "_mix.wav"), "-af", "alimiter=limit=0.84:attack=2:release=80:level=disabled", "-c:a", "pcm_s16le", str(W / "mix_v4.wav")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vin, "-i", str(W / "mix_v4.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                "-ar", "44100", "-shortest", "-movflags", "+faststart", vout], check=True)
print("ok", vout, "| LUFS grito antigo", round(lo_old, 1))

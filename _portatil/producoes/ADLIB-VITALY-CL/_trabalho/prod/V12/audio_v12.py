# -*- coding: utf-8 -*-
"""Refaz a voz da parte 1: vocals (demucs) com trechos trocados pela voz clonada + no_vocals; corta em FIM_S."""
import subprocess, numpy as np, json
SR = 48000; FIM_S = 1934 / 30
def le(p, extra=[]):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, *extra, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
voc = le("sep/htdemucs/orig/vocals.wav"); mus = le("sep/htdemucs/orig/no_vocals.wav")
def fala(p):
    a = le(p); env = np.abs(a).max(1)
    idx = np.where(env > 0.02)[0]; return a[max(0, idx[0] - 480): idx[-1] + 960]
def rms(x): return np.sqrt((x ** 2).mean() + 1e-12)
TROCAS = [  # (arquivo, inicio_fala, janela_ini, janela_fim)
    ("f1.mp3", 15.60, 15.45, 17.12),
    ("f2.mp3", 36.36, 36.28, 39.08),
]
log = []
for arq, t0, w0, w1 in TROCAS:
    a, b = int(w0 * SR), int(w1 * SR)
    ref = voc[int(t0 * SR):b]; ganho_ref = rms(ref[np.abs(ref).max(1) > 0.02]) if (np.abs(ref).max(1) > 0.02).any() else rms(ref)
    n = fala(arq)
    disp = w1 - t0 - 0.05
    tempo = 1.0
    if len(n) / SR > disp or len(n) / SR < 0.9 * disp:
        tempo = max(0.85, (len(n) / SR) / disp)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", arq, "-af", f"atempo={tempo:.4f}", "_tmp.wav"], check=True)
        n = fala("_tmp.wav")
    n = n * (ganho_ref / rms(n[np.abs(n).max(1) > 0.02]))
    f = np.ones(b - a); r = int(0.03 * SR); f[:r] = np.linspace(1, 0, r); f[-r:] = np.linspace(0, 1, r)
    f[r:-r] = 0
    voc[a:b] *= f[:, None]
    s = int(t0 * SR); m = min(len(n), b - s)
    fe = np.ones(m); k = int(0.015 * SR); fe[:k] = np.linspace(0, 1, k); fe[-k:] = np.linspace(1, 0, k)
    voc[s:s + m] += n[:m] * fe[:, None]
    log.append(dict(arquivo=arq, inicio=t0, janela=[w0, w1], dur_fala=round(m / SR, 3), tempo=round(tempo, 3)))
mix = (voc + mus[:len(voc)])[:int(FIM_S * SR)]
k = int(0.12 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
pk = np.abs(mix).max(); mix = mix / max(1.0, pk / 0.98)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "audio_parte1.wav"], input=mix.astype(np.float32).tobytes(), check=True)
print(json.dumps(log, ensure_ascii=False))

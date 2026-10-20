# -*- coding: utf-8 -*-
"""SFX sinteticos (sem direitos): whoosh.wav (0,35 s) e pop.wav (0,18 s), 48 kHz estereo, gerados com numpy."""
import wave
from pathlib import Path
import numpy as np

SR = 48000
OUT = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\producao\edicao\sfx")
rng = np.random.default_rng(7)


def salvar(nome, x, pan=0.0):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.89
    st = np.stack([x * (1 - max(pan, 0)), x * (1 + min(pan, 0))], 1)
    with wave.open(str(OUT / nome), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


def whoosh(dur=0.35):
    n = int(SR * dur)
    t = np.arange(n) / SR
    ruido = rng.standard_normal(n)
    # filtro passa-banda que varre 300 Hz -> 3,5 kHz -> 900 Hz (STFT em blocos)
    out = np.zeros(n)
    blk, hop = 1024, 256
    win = np.hanning(blk)
    freqs = np.fft.rfftfreq(blk, 1 / SR)
    for i in range(0, n - blk, hop):
        p = (i + blk / 2) / n
        fc = 300 * (3500 / 300) ** min(1, p / 0.6) if p < 0.6 else 3500 * (900 / 3500) ** ((p - 0.6) / 0.4)
        bw = fc * 0.9
        g = np.exp(-0.5 * ((freqs - fc) / bw) ** 2)
        seg = np.fft.irfft(np.fft.rfft(ruido[i:i + blk] * win) * g, blk)
        out[i:i + blk] += seg * win
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6 * (1 - 0.35 * t / dur)
    return out * env


def pop(dur=0.18):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 18) + 180          # queda rapida de tom
    fase = 2 * np.pi * np.cumsum(f) / SR
    corpo = np.sin(fase) * np.exp(-t * 28)
    clique = rng.standard_normal(n) * np.exp(-t * 400) * 0.5
    ataque = np.clip(t / 0.002, 0, 1)
    return (corpo + clique) * ataque


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    salvar("whoosh.wav", whoosh())
    salvar("pop.wav", pop())
    print("ok")

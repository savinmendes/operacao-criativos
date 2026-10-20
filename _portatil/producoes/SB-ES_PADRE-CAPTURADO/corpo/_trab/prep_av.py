# -*- coding: utf-8 -*-
import numpy as np, soundfile as sf, librosa
from plano2 import *
SR = 44100; (T / "avatar" / "in").mkdir(parents=True, exist_ok=True); tot = 0
for n in LINHAS:
    y, _ = librosa.load(T / "tts" / f"{n}.mp3", sr=SR, mono=True)
    y = np.concatenate([np.zeros(int(LEAD * SR)), y, np.zeros(2 * SR)])
    m, dur = mapa(n); z = np.zeros(int(dur * SR) + 10)
    for a, b, o in m:
        s = y[int(a * SR): int(b * SR)].copy(); k = int(0.008 * SR); s[:k] *= np.linspace(0, 1, k); s[-k:] *= np.linspace(1, 0, k)
        i = int(o * SR); z[i:i + len(s)] += s
    sf.write(T / "avatar" / "in" / f"{n}.wav", z, SR, subtype="PCM_16"); tot += dur
    print(n, "avatar", round(dur, 2), "s", [(round(a, 2), round(b, 2), round(o, 2)) for a, b, o in m])
print("total", round(tot, 1), "s")

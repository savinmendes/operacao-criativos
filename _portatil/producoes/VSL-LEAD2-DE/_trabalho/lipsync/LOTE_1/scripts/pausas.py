# -*- coding: utf-8 -*-
"""Pausas da fala DE (>= 0,27 s, pico-30 dB) de um trecho, em segundos da timeline nova: python pausas.py id ..."""
import sys, json, subprocess
from pathlib import Path
import numpy as np
AQ = Path(__file__).resolve().parent.parent
R = {}
for tid in sys.argv[1:]:
    D = AQ / "work" / tid; I = json.load(open(D / "info.json"))
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(D / "de_real.wav"), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.int16).astype(np.float32); h = 16000 // 30
    e = np.array([np.sqrt(np.mean(x[i:i + h] ** 2) + 1e-9) for i in range(0, len(x) - h + 1, h)])
    db = 20 * np.log10(e + 1e-9); fala = db > db.max() - 30
    t0 = I["q0"] / 30; out = []; k = 0
    while k < len(fala):
        if not fala[k]:
            j = k
            while j < len(fala) and not fala[j]: j += 1
            if j - k >= 8 and k > 0 and j < len(fala): out.append([round(t0 + k / 30, 2), round(t0 + j / 30, 2)])
            k = j
        else: k += 1
    R[tid] = out; print(tid, out)
json.dump(R, open(AQ / "_tmp" / "pausas_reprovados.json", "w"), indent=1)

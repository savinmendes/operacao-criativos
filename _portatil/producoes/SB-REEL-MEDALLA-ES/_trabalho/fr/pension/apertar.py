# -*- coding: utf-8 -*-
"""Encurta pausas longas de uma fala TTS (mp3 + .alinhamento.json) sem acelerar a voz.
uso: python apertar.py entrada.mp3 saida.wav [max_pausa=0.45] [manter=0.40]
Gera saida.wav + saida.alinhamento.json (tempos deslocados) e imprime os cortes."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
SR = 48000
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
MAXP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.45
KEEP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.40
al = json.loads(Path(str(src.with_suffix("")) + ".alinhamento.json").read_text(encoding="utf-8"))
ch, a0, a1 = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
# pausas = intervalos entre fim de uma letra e início da próxima letra (ignorando espaços/pontuação)
idx = [i for i, c in enumerate(ch) if c.isalnum()]
cortes = []
for i, j in zip(idx, idx[1:]):
    g0, g1 = a1[i], a0[j]
    if g1 - g0 > MAXP:
        # corta o meio da pausa, mantendo KEEP s no total; corte em ponto de menor energia
        m = (g0 + g1) / 2; rem = (g1 - g0) - KEEP
        c0, c1 = m - rem / 2, m + rem / 2
        cortes.append((round(c0, 3), round(c1, 3)))
def T(t):
    s = t
    for c0, c1 in cortes:
        if t >= c1: s -= c1 - c0
        elif t > c0: s -= t - c0
    return round(s, 3)
keep, s0 = [], 0.0
for c0, c1 in cortes:
    keep.append((s0, c0)); s0 = c1
keep.append((s0, len(x) / SR))
f = int(0.012 * SR); partes = []
for a, b in keep:
    seg = x[int(a * SR):int(b * SR)].copy()
    if len(seg) > 2 * f:
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    partes.append(seg)
y = np.concatenate(partes)
raw = dst.with_suffix(".f32"); raw.write_bytes(y.astype(np.float32).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(raw), "-c:a", "pcm_s16le", str(dst)], check=True)
raw.unlink()
al2 = dict(characters=ch, character_start_times_seconds=[T(t) for t in a0], character_end_times_seconds=[T(t) for t in a1])
Path(str(dst.with_suffix("")) + ".alinhamento.json").write_text(json.dumps(al2, ensure_ascii=False), encoding="utf-8")
print("cortes", cortes, "dur", round(len(y) / SR, 3))

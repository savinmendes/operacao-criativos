# -*- coding: utf-8 -*-
"""<id>.mp3 + alinhamento -> <id>.wav (48k estéreo) com pausas internas <= MAXP, início 0,03 s, cauda 0,12 s; <id>.palavras.json"""
import sys, json, subprocess
import numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; SR = 48000
MAXP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.22

def palavras(al):
    W = []; cur = None
    for ch, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append(cur); cur = None
            continue
        if cur is None: cur = [ch, s, e]
        else: cur[0] += ch; cur[2] = e
    if cur: W.append(cur)
    return W

def proc(i):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(AQ / f"{i}.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32).copy()
    W = palavras(json.loads((AQ / f"{i}.alinhamento.json").read_text(encoding="utf-8")))
    # segmentos de fala: [ini-0.03, fim+?] ; mantém tudo entre palavras, mas encurta gaps
    pedacos = []; P = []; t_out = 0.0
    ini = max(0.0, W[0][1] - 0.03)
    cortes = []   # (a, b) trechos a remover
    for (w1, s1, e1), (w2, s2, e2) in zip(W, W[1:]):
        g = s2 - e1
        if g > MAXP:
            a = e1 + (MAXP / 2); b = s2 - (MAXP / 2); cortes.append((a, b))
    fim = min(len(x) / SR, W[-1][2] + 0.12)
    segs = []; cur = ini
    for a, b in cortes: segs.append((cur, a)); cur = b
    segs.append((cur, fim))
    xf = int(0.008 * SR); y = []
    for a, b in segs:
        s = x[int(a * SR):int(b * SR)].copy()
        if len(s) > 2 * xf: s[:xf] *= np.linspace(0, 1, xf); s[-xf:] *= np.linspace(1, 0, xf)
        y.append(s)
    y = np.concatenate(y)
    def mapa(t):
        off = ini
        for a, b in cortes:
            if t >= b: off += b - a
            elif t > a: return a - off
        return t - off
    P = [dict(w=w, ini=round(mapa(s), 3), fim=round(mapa(e), 3)) for w, s, e in W]
    raw = AQ / f"_{i}.f32"; raw.write_bytes(y.astype(np.float32).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(raw), "-ac", "2", "-c:a", "pcm_s16le", str(AQ / f"{i}.wav")], check=True)
    raw.unlink()
    (AQ / f"{i}.palavras.json").write_text(json.dumps(P, ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, round(len(y) / SR, 2), "s; cortes", [(round(a, 2), round(b - a, 2)) for a, b in cortes])

for i in sys.argv[1].split(","): proc(i)

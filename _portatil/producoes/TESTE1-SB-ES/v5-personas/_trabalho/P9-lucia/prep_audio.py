# -*- coding: utf-8 -*-
"""audio/<id>.mp3 + alinhamento -> audio/<id>.wav (pausas internas > MAXP encurtadas a MAXP, cauda 0,12 s) + audio/<id>.palavras.json"""
import json, subprocess, sys
import numpy as np
from pathlib import Path
A = Path(__file__).resolve().parent / "audio"; SR = 48000
def palavras(d):
    W = []; cur = None
    for ch, s, e in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append(cur); cur = None
            continue
        if cur is None: cur = [ch, s, e]
        else: cur[0] += ch; cur[2] = e
    if cur: W.append(cur)
    return W
def prep(i, maxp=0.25, cauda=0.12):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(A / f"{i}.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32).copy()
    W = palavras(json.loads((A / f"{i}.alinhamento.json").read_text(encoding="utf-8")))
    cortes = []
    for a, b in zip(W, W[1:]):
        g = b[1] - a[2]
        if g > maxp + 0.02:
            c0 = a[2] + 0.06; c1 = c0 + (g - maxp); cortes.append((c0, c1))
    ini = max(0.0, W[0][1] - 0.05)
    segs = []; t = ini
    for c0, c1 in cortes: segs.append((t, c0)); t = c1
    segs.append((t, W[-1][2] + cauda))
    xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for a, b in segs:
        s = x[int(a * SR):int(b * SR)].copy()
        if len(out) and xf:
            w = np.linspace(0, 1, xf); s[:xf] = out[-xf:] * (1 - w) + s[:xf] * w; out = out[:-xf]
        out = np.concatenate([out, s])
    f = int(0.03 * SR); out[-f:] *= np.linspace(1, 0, f)
    def sh(tt):
        d = ini
        for c0, c1 in cortes:
            if tt >= c1: d += c1 - c0
            elif tt > c0: return c0 - d
        return tt - d
    P = [dict(w=w, ini=round(sh(s), 3), fim=round(sh(e), 3)) for w, s, e in W]
    raw = A / f"{i}.f32"; raw.write_bytes(out.astype(np.float32).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(raw), "-ac", "2", "-c:a", "pcm_s16le", str(A / f"{i}.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(raw), "-c:a", "libmp3lame", "-b:a", "192k", str(A / f"{i}_hg.mp3")], check=True)
    raw.unlink()
    (A / f"{i}.palavras.json").write_text(json.dumps(P, ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, f"{len(out)/SR:.2f}s", f"{len(cortes)} pausas encurtadas", P[-1]["fim"])
for i in (sys.argv[1:] or ["R00", "R01", "LV1", "L01", "L02", "L03", "L04", "R02"]): prep(i)

# -*- coding: utf-8 -*-
"""R00b.mp3 (Gabriela, est .5 estilo .2 vel 1.16) -> R00.wav: pausa após 'impactantes:' 0,30 -> 0,22 s, cauda cortada em 3,82 s.
Gera palavras.json (tempos do alinhamento ElevenLabs ajustados)."""
import json, subprocess
import numpy as np
from pathlib import Path
A = Path(__file__).resolve().parent / "audio"; SR = 48000; CUT = (1.36, 1.44); FIM = 3.82
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(A / "R00b.mp3"), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32).copy()
a, b = int(CUT[0] * SR), int(CUT[1] * SR); xf = int(0.01 * SR)
w = np.linspace(0, 1, xf); mid = x[a - xf:a] * (1 - w) + x[b - xf:b] * w
y = np.concatenate([x[:a - xf], mid, x[b:]])[:int(FIM * SR)]
f = int(0.04 * SR); y[-f:] *= np.linspace(1, 0, f)
(A / "R00.f32").write_bytes(y.astype(np.float32).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", str(A / "R00.f32"), "-ac", "2", "-c:a", "pcm_s16le", str(A / "R00.wav")], check=True)
(A / "R00.f32").unlink()
d = json.loads((A / "R00b.alinhamento.json").read_text(encoding="utf-8")); W = []; cur = None
for ch, s, e in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
    if ch.isspace():
        if cur: W.append(cur); cur = None
        continue
    if cur is None: cur = [ch, s, e]
    else: cur[0] += ch; cur[2] = e
if cur: W.append(cur)
dc = CUT[1] - CUT[0]; sh = lambda t: t - dc if t > CUT[0] else t
P = [dict(w=w, ini=round(sh(s), 3), fim=round(min(sh(e), FIM - 0.05), 3)) for w, s, e in W]
(A / "palavras.json").write_text(json.dumps(P, ensure_ascii=False, indent=0), encoding="utf-8")
print(len(y) / SR, P[-1])

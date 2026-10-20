# -*- coding: utf-8 -*-
"""Trilhas de voz por personagem na linha do tempo final (48 kHz estéreo float) -> voz/trilha_<p>.wav"""
import subprocess, numpy as np
from pathlib import Path
import plano
AQ = Path(__file__).resolve().parent; SR = 48000
def load(p, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
def trilhas():
    N = int(plano.TOTAL * SR) + SR; T = {}
    for i, d in plano.LIN.items():
        a = load(AQ / "voz" / "c" / f"{i}.wav"); p = d["p"]
        T.setdefault(p, np.zeros((N, 2), np.float32)); s = int(d["T0"] * SR)
        T[p][s:s + len(a)] += a[:N - s]
    return T
def salvar(a, out):
    raw = Path(str(out) + ".f32"); raw.write_bytes(a.astype(np.float32).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-c:a", "pcm_s16le", str(out)], check=True); raw.unlink()
if __name__ == "__main__":
    for p, a in trilhas().items(): salvar(a, AQ / "voz" / f"trilha_{p}.wav"); print(p)

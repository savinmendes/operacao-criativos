# -*- coding: utf-8 -*-
"""áudio da briga com voz única: patrona STS (Karly) + '¿Rezas' colado; Carmen STS (Alisson) + 'créame' colado; fundo demucs"""
import subprocess, numpy as np
SR = 44100
def L(p, ch=2):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, ch).copy()
voc = L("htdemucs/briga2/vocals.wav"); nv = L("htdemucs/briga2/no_vocals.wav")
def rms(x): return float(np.sqrt((x ** 2).mean()) + 1e-9)
new = voc.copy(); x = int(0.04 * SR); w = np.linspace(0, 1, x)[:, None]
for arq, t0, t1 in (("patrona_fix.wav", 0.9, 6.05), ("carmen_fix.wav", 6.0, 9.6)):
    st = L(arq); a = int(t0 * SR); n = min(len(st), int((t1 - t0) * SR)); st = st[:n]
    seg = voc[a:a + n]; st = st * (rms(seg) / rms(st))
    st[:x] = seg[:x] * (1 - w) + st[:x] * w; st[-x:] = st[-x:] * (1 - w) + seg[-x:] * w
    new[a:a + n] = st
out = new + nv
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", "briga_audio_sts.wav"], input=out.astype(np.float32).tobytes(), check=True)
print("ok")

# -*- coding: utf-8 -*-
"""Seedance da briga: (1) fala da Rosa (6,75-10,90 s) trocada pela voz Luisa via STS (demucs; fundo original mantido);
(2) câmera lenta 0-2,80 s (x1,589 -> 4,45 s) para a REPORTERA em PiP terminar antes da clienta (que começa em 2,88 s no take).
Saída: takes/seedance_slow.mp4 (vídeo 30 fps, sem áudio) + audio/briga_audio.wav (48 kHz)"""
import subprocess, numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; T = AQ / "takes" / "seedance_briga.mp4"; SR = 48000
S0, S1 = 6.75, 10.90; LENTO = 2.80; F = 4.45 / 2.80
def load(p, ss=0, t=None):
    c = ["ffmpeg", "-v", "error", "-ss", str(ss)] + (["-t", str(t)] if t else []) + ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(c, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
a = load(T); vz = load(AQ / "sts" / "rosa_luisa.wav")
def lufs(x):
    r = AQ / "audio" / "_l.f32"; r.write_bytes(x.astype(np.float32).tobytes())
    o = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(r), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    r.unlink(); return float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
vz *= 10 ** ((-13.5 - lufs(vz)) / 20)          # STS devolve ~8 dB abaixo do original: Rosa a -17 LUFS (clienta grita a ~-12)
v = vz + load(AQ / "sts" / "rosa_luisa_fundo.wav")
i0, i1 = int(S0 * SR), int(S0 * SR) + len(v); xf = int(0.03 * SR)
w = np.ones(len(v), np.float32); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
seg = a[i0:i1]; n = min(len(seg), len(v)); a[i0:i0 + n] = seg[:n] * (1 - w[:n, None]) + v[:n] * w[:n, None]
raw = AQ / "audio" / "_b.f32"; raw.write_bytes(a.astype(np.float32).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-filter_complex",
                f"[0:a]atrim=0:{LENTO},asetpts=PTS-STARTPTS,atempo={1 / F:.5f}[x];[0:a]atrim={LENTO},asetpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=0:a=1",
                "-c:a", "pcm_s16le", str(AQ / "audio" / "briga_audio.wav")], check=True); raw.unlink()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(T), "-filter_complex",
                f"[0:v]trim=0:{LENTO},setpts=(PTS-STARTPTS)*{F:.5f},minterpolate=fps=30:mi_mode=blend[x];[0:v]trim={LENTO},setpts=PTS-STARTPTS,fps=30[y];[x][y]concat=n=2:v=1:a=0",
                "-an", "-c:v", "libx264", "-crf", "10", "-preset", "fast", str(AQ / "takes" / "seedance_slow.mp4")], check=True)
print("ok, deslocamento depois de", LENTO, "s:", round(4.45 - LENTO, 3))

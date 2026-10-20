# -*- coding: utf-8 -*-
"""Entradas HeyGen: ls/in/v_<job>.mp4 (rosto recortado + ÁUDIO ORIGINAL do trecho) e ls/in/a_<job>.wav (fala nova da janela, silêncio até a duração do vídeo)."""
import subprocess, sys, numpy as np, soundfile as sf, librosa
from plano import *
SR = 44100
def linha(n):
    L = LINHAS[n]; y, _ = librosa.load(T / "tts" / f"{L['tts']}.mp3", sr=SR, mono=True)
    return np.concatenate([np.zeros(int(L["lead"] * SR)), y, np.zeros(2 * SR)])
so = set(sys.argv[1:])
for n, j in JOBS.items():
    if so and n not in so: continue
    kind, q0, q1 = j["src"]; dur = (q1 - q0 + 1) / 30
    out = T / "ls" / "in" / f"v_{n}.mp4"
    if kind == "base":
        x, y, w, h = j["crop"]; t0 = q0 / 30
        vf = rf"select='between(n\,{q0}\,{q1})',setpts=N/30/TB,crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos,format=yuv420p"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(BASE), "-i", str(GA / "audio" / "audio_orig.wav"), "-filter_complex",
                        f"[0:v]{vf}[v];[1:a]atrim={t0}:{t0 + dur},asetpts=PTS-STARTPTS[a]", "-map", "[v]", "-map", "[a]", "-r", "30",
                        "-c:v", "libx264", "-crf", "14", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
    else:
        t0 = (q0 - 239) / 30
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-i", str(AVC), "-t", f"{dur:.4f}", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
    y = linha(j["linha"]); jan = j["janela"] if isinstance(j["janela"], list) else [j["janela"]]
    parts = []
    for a, b in jan:
        s = y[int(a * SR): int(b * SR)].copy(); k = int(0.01 * SR); s[:k] *= np.linspace(0, 1, k); s[-k:] *= np.linspace(1, 0, k); parts.append(s)
    z = np.concatenate(parts); N = int(dur * SR)
    if len(z) > N: print("  aviso: janela maior que o vídeo", n, len(z) / SR, dur); z = z[:N]
    z = np.pad(z, (0, N - len(z)))
    sf.write(T / "ls" / "in" / f"a_{n}.wav", z, SR, subtype="PCM_16")
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]))
    print(n, "video", round(d, 3), "esperado", round(dur, 3))

# Entradas do lipsync HeyGen: video do original com AUDIO PT original + audio ES separado (mesma duracao)
import subprocess, numpy as np, soundfile as sf, librosa
from pathlib import Path
P = Path(__file__).resolve().parent; I = P / "in"; ORIG = str(P.parents[2] / "01_628k_DQ7ptOAkVeh.mp4"); TT = P.parent / "tts"
SR = 44100
def es(nome, partes, dur):
    out = np.zeros(int(dur * SR))
    for fonte, a, b, t0 in partes:
        y, _ = librosa.load(TT / f"{fonte}.mp3", sr=SR); s = y[int(a * SR):int(b * SR)]
        k = int(0.01 * SR); s = s.copy(); s[:k] *= np.linspace(0, 1, k); s[-k:] *= np.linspace(1, 0, k)
        n = min(len(s), len(out) - int(t0 * SR)); out[int(t0 * SR):int(t0 * SR) + n] += s[:n]
    sf.write(I / f"es_{nome}.wav", out, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(I / f"es_{nome}.wav"), "-b:a", "192k", str(I / f"es_{nome}.mp3")], check=True)
def vid(nome, t0, dur, crop=None):
    vf = "scale=in_color_matrix=bt709:out_color_matrix=bt709"
    if crop: x, y, w, h = crop; vf = f"crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-i", ORIG, "-t", f"{dur}", "-vf", vf, "-r", "30",
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", str(I / f"pt_{nome}.mp4")], check=True)
# RA: reporter 0.0-2.0 s (rosto ate o glitch); fala ES comeca em 0.10
vid("RA", 0.0, 2.0, (330, 640, 288, 512)); es("RA", [("R1", 0.0, 1.90, 0.10)], 2.0)
# DA: dono 12.85-18.80 ; D1 inteiro (0-5.55) a partir de 0.15
vid("DA", 12.85, 5.95); es("DA", [("D1", 0.0, 5.60, 0.15)], 5.95)
# DB: dono 18.80-24.30 ; D2 'La aprendi ... en vivo.' (5.90-11.10) a partir de 0.15
vid("DB", 18.80, 5.50); es("DB", [("D2", 5.90, 11.10, 0.15)], 5.50)
for p in sorted(I.glob("*")): print(p.name, p.stat().st_size)

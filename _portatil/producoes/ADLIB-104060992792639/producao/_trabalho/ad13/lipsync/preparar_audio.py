import subprocess, sys
sys.path.insert(0, '.')
from segs import SEGS
for n, q, a, b in SEGS:
    t0, d = a / 30, (b - a) / 30
    src = 'narr_jesus.wav' if q == 'jesus' else 'narr_mulher.wav'
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-t", f"{d:.4f}", "-i", src, "-ac", "1", "-ar", "44100",
                    "-c:a", "libmp3lame", "-b:a", "192k", f"lipsync/es_{n}.mp3"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-t", f"{d:.4f}", "-i", "_audio/orig.wav", "-ac", "2", "-ar", "44100",
                    "-c:a", "pcm_s16le", f"lipsync/pt_{n}.wav"], check=True)
    print(n, round(d, 2))

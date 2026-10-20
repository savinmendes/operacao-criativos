# -*- coding: utf-8 -*-
"""Revisão: whisper es + en no AD final, busca de termos proibidos, silêncio no fim e folha 1 quadro/s."""
import re, subprocess, sys
from pathlib import Path
from faster_whisper import WhisperModel
from PIL import Image, ImageDraw
v = sys.argv[1]
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for lang in ("es", "en"):
    segs, _ = m.transcribe(v, language=lang, vad_filter=False, beam_size=5)
    txt = " ".join(s.text.strip() for s in segs)
    print(f"[{lang}] {txt}\n")
    if lang == "es":
        proib = r"precio|\$|d[oó]lar|chile|m[eé]xico|colombia|am[eé]rica|tiktok|link|enlace|navidad|a[ñn]o nuevo|descuento|agotad|stock|meses|semanas|sin sol|100 ?%|cien por ciento|wyze\.com"
        print("PROIBIDOS:", re.findall(proib, txt, re.I) or "nenhum")
# silêncio no fim
out = subprocess.run(["ffmpeg", "-i", v, "-af", "silencedetect=n=-45dB:d=0.7", "-f", "null", "-"], capture_output=True, text=True).stderr
print("SILENCIOS:", re.findall(r"silence_(?:start|end): [\d.]+", out))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
print("DUR", dur)
# folha 1 q/s
tmp = Path(v).with_suffix("")
fs = []
for t in range(int(dur) + 1):
    t = min(t, dur - 0.05)
    o = f"{tmp}_f{t:05.1f}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", v, "-frames:v", "1", "-vf", "scale=180:320", o])
    fs.append((t, o))
cols = 9
rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * 180, rows * 320))
for i, (t, o) in enumerate(fs):
    im = Image.open(o); d = ImageDraw.Draw(im); d.text((4, 4), f"{t:.0f}s", fill=(255, 255, 0))
    S.paste(im, ((i % cols) * 180, (i // cols) * 320)); Path(o).unlink()
dest = sys.argv[2]
S.save(dest, quality=85)
print("folha", dest)

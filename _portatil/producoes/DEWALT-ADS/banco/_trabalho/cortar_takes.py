# -*- coding: utf-8 -*-
"""Corta os takes do banco a partir das fontes 720x1280 ja limpas. Sem audio, 30 fps, h264 crf 18, etiqueta bt709/tv
(sem conversao de matriz: yuv -> yuv). Uso: python cortar_takes.py takes.json"""
import sys, json, subprocess
from pathlib import Path
T = json.load(open(sys.argv[1], encoding="utf-8")); BANCO = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\banco")
for t in T:
    out = BANCO / t["arquivo"]
    if out.exists() and not t.get("refazer"): continue
    vel = t.get("velocidade", 1.0); dur = t["fim"] - t["ini"]
    vf = f"setpts=PTS/{vel}," if vel != 1.0 else ""
    vf += "fps=30,format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t['ini']:.3f}", "-t", f"{dur:.3f}", "-i", t["fonte"], "-an", "-vf", vf,
                    "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-color_range", "tv", "-colorspace", "bt709",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", str(out)], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                             capture_output=True, text=True).stdout)
    print(f"{t['arquivo']}: {d:.2f}s", flush=True)

# -*- coding: utf-8 -*-
"""Corta takes (início, quadros) do up720.mp4 de um AD, estende com quadro congelado até >=3,4 s e gera prévia.
  python cortar_takes.py ad04 7.367:190 13.7:78 ...   -> ad04/flora/t1.mp4, t2.mp4 ... + prev.jpg"""
import subprocess, sys
from pathlib import Path
P = Path(__file__).parent / sys.argv[1]
(P / "flora").mkdir(exist_ok=True)
prevs = []
for i, s in enumerate(sys.argv[2:], 1):
    ini, q = s.split(":"); ini = float(ini); q = int(q); d = q / 30
    pad = max(0.0, 3.4 - d)
    o = P / "flora" / f"t{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-t", f"{d:.4f}", "-i", str(P / "up720.mp4"), "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}", "-an", "-c:v", "libx264", "-crf", "14",
                    "-pix_fmt", "yuv420p", "-r", "30", str(o)], check=True)
    j = P / "flora" / f"t{i}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d/2:.2f}", "-i", str(o), "-frames:v", "1", "-vf", "scale=200:-1", str(j)], check=True)
    prevs.append(str(j))
args = sum([["-i", p] for p in prevs], [])
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f"hstack={len(prevs)}" if len(prevs) > 1 else "null", str(P / "flora" / "prev.jpg")], check=True)
print("ok", len(prevs))


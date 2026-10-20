# -*- coding: utf-8 -*-
"""python baixar_folha.py nome url [n_quadros]  -> takes/nome.mp4 + takes/nome_folha.jpg (grade 5 col)"""
import subprocess, sys, urllib.request
from pathlib import Path
D = Path(__file__).resolve().parent / "takes"
D.mkdir(exist_ok=True)
nome, url = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 15
mp4 = D / f"{nome}.mp4"
if url.endswith(".png"):
    mp4 = D / f"{nome}.png"
urllib.request.urlretrieve(url, mp4)
if mp4.suffix == ".png":
    sys.exit(0)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                           capture_output=True, text=True).stdout)
info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
                       "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip()
fps = n / dur
rows = (n + 4) // 5
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf",
                f"fps={fps:.4f},scale=300:-1,tile=5x{rows}",
                "-frames:v", "1", str(D / f"{nome}_folha.jpg")], check=True)
print(nome, f"{dur:.2f}s", info)


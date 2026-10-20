# -*- coding: utf-8 -*-
"""Folha com N quadros por take (para achar texto queimado ao longo do take).
  python folha_takes.py saida.jpg idx1,idx2,...  (índices do inventario.json) [--n 5]"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

AQ = Path(__file__).parent
inv = json.load(open(AQ / "inventario.json", encoding="utf-8"))
saida = sys.argv[1]
ids = [int(x) for x in sys.argv[2].split(",")]
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
tw, th = 120, 213
tmp = AQ / "_fol"; tmp.mkdir(exist_ok=True)
sheet = Image.new("RGB", (N * tw + 40, len(ids) * (th + 4)), "white")
dr = ImageDraw.Draw(sheet)
for r, i in enumerate(ids):
    t = inv[i]; d = t["dur"]
    dr.text((2, r * (th + 4) + 5), str(i), fill="red")
    for k in range(N):
        ts = d * (k + 0.5) / N
        p = tmp / f"{i}_{k}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.2f}", "-i", t["f"], "-frames:v", "1",
                        "-vf", f"scale={tw}:{th}", str(p)])
        sheet.paste(Image.open(p), (40 + k * tw, r * (th + 4)))
sheet.save(saida, quality=80)

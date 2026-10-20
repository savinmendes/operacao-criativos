# -*- coding: utf-8 -*-
"""Base dos ADs 08/10 (Wyze, EN -> ES LATAM): faixa opaca sobre a legenda em inglês,
fundo sem voz (demucs) + narração nova, corte no fim da fala, alinhamento deslocado.
  python preparar_base_08_10.py 08|10"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 720, 1280
CFG = {  # faixa em px 720x1280 (cobre a caixa de legenda original com folga)
    "08": dict(topo=958, base=1102),
    "10": dict(topo=1022, base=1222),
}
n = sys.argv[1]
c = CFG[n]
P = Path(__file__).resolve().parent
T = P / f"ad{n}"
ORIG = P.parent.parent / "originais" / f"{n}.mp4"
NARR = P / "ad08" / "narr.mp3"          # mesma narração nos dois
T0 = 0.30                              # início da fala
FIM = 41.70                            # ~0,5 s após a última palavra (sem silêncio no fim)

# faixa quase opaca (alpha 252) com bordas suaves de 14 px
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
g = 14
for y in range(c["topo"] - g, c["base"] + g):
    if y < c["topo"]:
        a = int(252 * (y - (c["topo"] - g)) / g)
    elif y >= c["base"]:
        a = int(252 * (c["base"] + g - y) / g)
    else:
        a = 252
    d.line([(0, y), (W, y)], fill=(12, 12, 12, a))
img.save(T / "faixa.png")

al = json.load(open(P / "ad08" / "narr.alinhamento.json", encoding="utf-8"))
for k in ("character_start_times_seconds", "character_end_times_seconds"):
    al[k] = [round(t + T0, 3) for t in al[k]]
json.dump(al, open(T / "alinhamento.json", "w", encoding="utf-8"), ensure_ascii=False)

fundo = T / "sep" / "htdemucs" / f"orig_{n}" / "no_vocals.wav"
fc = ("[0:v][3:v]overlay=0:0[v];"
      "[1:a]volume=1.0,aresample=48000[bg];"
      f"[2:a]adelay={int(T0*1000)}|{int(T0*1000)},aresample=48000[nv];"
      "[bg][nv]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=" + f"{FIM-0.3:.2f}" + ":d=0.3[a]")
saida = T / "corpo.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-t", f"{FIM}", "-i", str(ORIG),
                "-t", f"{FIM}", "-i", str(fundo), "-i", str(NARR), "-i", str(T / "faixa.png"),
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{FIM}",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", str(saida)], check=True)
print("ok", saida)

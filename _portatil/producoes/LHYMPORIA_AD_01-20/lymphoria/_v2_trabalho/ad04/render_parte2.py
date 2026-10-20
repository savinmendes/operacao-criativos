# -*- coding: utf-8 -*-
"""Parte 2 (fim novo): fotos do produto em 9:16 com zoom lento + narração.
  python render_parte2.py narr.mp3 saida.mp4 img1.jpg:0 img2.jpg:8.15 ...   (imagem:segundo em que entra)
Foto quadrada em cima (y 30..970), fundo = a mesma foto ampliada e desfocada; legenda/selo/setas ficam embaixo."""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

narr, saida = sys.argv[1], sys.argv[2]
cenas = [(a.rsplit(":", 1)[0], float(a.rsplit(":", 1)[1])) for a in sys.argv[3:]]
FPS, W, H, LADO, TOPO, CAUDA, XF = 30, 1080, 1920, 940, 30, 0.6, 0.25

d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", narr],
                         capture_output=True, text=True).stdout) + CAUDA
fins = [c[1] for c in cenas[1:]] + [d]
imgs = [Image.open(p).convert("RGB") for p, _ in cenas]
fundos = []
for im in imgs:
    f = im.resize((H, H), Image.LANCZOS).crop(((H - W) // 2, 0, (H - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
    f = Image.blend(f, Image.new("RGB", f.size, (0, 0, 0)), 0.35)
    fundos.append(f)


def quadro(i, t):
    ini, fim = cenas[i][1], fins[i]
    u = (t - ini) / max(0.01, fim - ini)
    z = 1.0 + 0.08 * u
    im = imgs[i]
    s = im.size[0]
    c = s / z
    o = (s - c) / 2
    fg = im.crop((o, o, o + c, o + c)).resize((LADO, LADO), Image.LANCZOS)
    fr = fundos[i].copy()
    fr.paste(fg, ((W - LADO) // 2, TOPO))
    return fr


ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-i", narr, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16",
                       "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                       "-ac", "2", "-af", f"apad=pad_dur={CAUDA}", "-t", f"{d:.3f}", saida], stdin=subprocess.PIPE)
for k in range(int(d * FPS)):
    t = k / FPS
    i = max(j for j, c in enumerate(cenas) if c[1] <= t)
    fr = quadro(i, t)
    if i > 0 and t - cenas[i][1] < XF:                         # transição curta entre fotos
        fr = Image.blend(quadro(i - 1, t), fr, (t - cenas[i][1]) / XF)
    ff.stdin.write(np.asarray(fr).tobytes())
ff.stdin.close()
ff.wait()
print("ok:", saida, f"{d:.2f}s")

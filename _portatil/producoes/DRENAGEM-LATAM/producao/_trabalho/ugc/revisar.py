# -*- coding: utf-8 -*-
"""Revisão do UGC final: whisper (es) + palavras proibidas + folha de contato (1 quadro a cada 2 s)
+ silêncio no fim + quadros soltos perto dos cortes de inserto.   python revisar.py NN"""
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
nn = sys.argv[1]
final = glob.glob(str(AQUI.parent.parent / f"UGC {nn} - *.mp4"))[0]
wk = AQUI / f"ugc{nn}"

from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(final, language="es")
txt = " ".join(s.text.strip() for s in segs)
(wk / "whisper_final.txt").write_text(txt, encoding="utf-8")
proib = ["maya", "verra", "sesenta", "60 d", "45 d", "estados unidos", "ozempic", "tiktok", "cofepris", "cáncer",
         "cancer", "precio", "link", "\\$", "kilo", "libra", "cura"]
achados = [p for p in proib if re.search(p, txt, re.I)]
print("WHISPER:", txt)
print("PROIBIDAS:", achados or "nenhuma")

# silêncio no fim
out = subprocess.run(["ffmpeg", "-i", final, "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                     "csv=p=0", final]).decode())
sil = re.findall(r"silence_start: ([\d.]+)", out)
fim_sil = [float(s) for s in sil if float(s) > dur - 3]
print(f"DURAÇÃO: {dur:.2f}s | silêncio nos últimos 3 s: {fim_sil or 'não'}")

# folha de contato
c = cv2.VideoCapture(final)
fps = c.get(5)
ts = np.arange(0, dur, 2.0)
cols = 9
W, H = 160, 284
S = Image.new("RGB", (cols * W, ((len(ts) + cols - 1) // cols) * (H + 18)), "white")
fnt = ImageFont.truetype("arial.ttf", 13)
for i, t in enumerate(ts):
    c.set(1, int(t * fps))
    ok, im = c.read()
    if not ok:
        continue
    x, y = (i % cols) * W, (i // cols) * (H + 18)
    S.paste(Image.fromarray(cv2.cvtColor(cv2.resize(im, (W, H)), cv2.COLOR_BGR2RGB)), (x, y + 18))
    ImageDraw.Draw(S).text((x + 3, y + 2), f"{t:.0f}s", fill="black", font=fnt)
S.save(wk / "folha_final.jpg", quality=85)

# quadros nas bordas de cada inserto (último quadro antes, 1º e último dentro, 1º depois)
ins = json.load(open(wk / "insertos.json", encoding="utf-8"))
B = Image.new("RGB", (len(ins) * 4 * 120, 213 + 16), "white")
for k, (t0, d, clipe) in enumerate(ins):
    for j, t in enumerate([t0 - 1 / fps, t0 + 0.01, t0 + d - 1 / fps, t0 + d + 0.01]):
        c.set(1, int(round(t * fps)))
        ok, im = c.read()
        if ok:
            B.paste(Image.fromarray(cv2.cvtColor(cv2.resize(im, (120, 213)), cv2.COLOR_BGR2RGB)),
                    ((k * 4 + j) * 120, 16))
    ImageDraw.Draw(B).text((k * 480 + 3, 1), f"{clipe} {t0:.2f}+{d:.1f}", fill="black", font=fnt)
B.save(wk / "bordas_insertos.jpg", quality=85)
print("folhas:", wk / "folha_final.jpg", wk / "bordas_insertos.jpg")

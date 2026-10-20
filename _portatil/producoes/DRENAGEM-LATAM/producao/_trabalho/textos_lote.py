# -*- coding: utf-8 -*-
"""Troca vários textos queimados (legenda) numa passada só.
  python textos_lote.py entrada.mp4 saida.mp4 trocas.json
trocas: [{"de":s,"ate":s,"caixa":"x0,y0,x1,y1","texto":"linha1\\nlinha2","tipo":"branco"|"caixa"|"limpar",
          "px":40,"fonte":"Poppins-Medium.ttf","contorno":2}]
- branco: apaga letras brancas na caixa (inpaint) e escreve branco com contorno escuro (legenda sem caixa).
- caixa: desenha caixa branca arredondada com texto azul-marinho (legenda estilo "caixa branca"), cobrindo a antiga.
- limpar: só apaga as letras brancas (sem texto novo).
Áudio copiado."""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
ent, sai, js = sys.argv[1], sys.argv[2], sys.argv[3]
T = json.load(open(js, encoding="utf-8-sig"))
cap = cv2.VideoCapture(ent)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
for t in T:
    t["i0"], t["i1"] = int(round(t["de"] * fps)), int(round(t["ate"] * fps))
    t["bx"] = list(map(int, t["caixa"].split(",")))
    t["font"] = ImageFont.truetype(str(FONTS / t.get("fonte", "Poppins-Medium.ttf")), int(t.get("px", 40)))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", sai], stdin=subprocess.PIPE)
i = 0
n = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    for t in T:
        if not (t["i0"] <= i <= t["i1"]):
            continue
        n += 1
        x0, y0, x1, y1 = t["bx"]
        tipo = t.get("tipo", "branco")
        if tipo in ("branco", "limpar"):
            reg = im[y0:y1, x0:x1]
            letras = (reg.min(2) > 195).astype(np.uint8)
            m = np.zeros(im.shape[:2], np.uint8)
            m[y0:y1, x0:x1] = cv2.dilate(letras, np.ones((9, 9), np.uint8))
            im = cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)
        if tipo == "limpar":
            continue
        pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(pil)
        txt = t["texto"]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if tipo == "caixa":
            bb = d.multiline_textbbox((0, 0), txt, font=t["font"], align="center")
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            px, py = 14, 8
            rx0, ry0 = min(x0, cx - tw / 2 - px), min(y0, cy - th / 2 - py)
            rx1, ry1 = max(x1, cx + tw / 2 + px), max(y1, cy + th / 2 + py)
            if t.get("ajustar", True):  # caixa do tamanho do texto novo, mas sempre cobrindo a antiga
                pass
            d.rounded_rectangle((rx0, ry0, rx1, ry1), radius=10, fill=(255, 255, 255))
            d.multiline_text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, font=t["font"], fill=(28, 32, 120),
                             align="center")
        else:
            c = int(t.get("contorno", 2))
            bb = d.multiline_textbbox((0, 0), txt, font=t["font"], stroke_width=c, align="center", spacing=2)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            d.multiline_text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, font=t["font"], fill=(255, 255, 255),
                             stroke_width=c, stroke_fill=(20, 20, 20), align="center", spacing=2)
        im = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    ff.stdin.write(im.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print(f"ok: {sai} | {n} quadros alterados")

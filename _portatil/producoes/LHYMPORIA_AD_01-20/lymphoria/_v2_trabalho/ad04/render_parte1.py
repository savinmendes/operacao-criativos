# -*- coding: utf-8 -*-
"""Parte 1 do AD: trecho original 0..CORTE s, ampliado para 1080x1920, com a faixa do rótulo
do concorrente coberta por "LYMPHORIA" (posição vinda de rastreio.json, interpolada em buracos curtos).

  python render_parte1.py <video_360p> <rastreio.json> <corte_s> <saida.mp4> [--preview t1,t2,...]
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, rast, corte, saida = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
preview = None
if "--preview" in sys.argv:
    preview = [float(t) for t in sys.argv[sys.argv.index("--preview") + 1].split(",")]

FONTE = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf")
TW, TH = 93, 19            # tamanho da faixa no quadro de referência (360p)
LIM = 0.72                 # score mínimo de match confiável
GAP = 45                   # buraco máximo (quadros) a interpolar dentro do mesmo plano
ESC = 3                    # 360x640 -> 1080x1920

r = {int(k): v for k, v in json.load(open(rast)).items()}
bons = {k: v for k, v in r.items() if v[3] >= LIM}
ks = sorted(bons)
caixa = {}
for k in ks:
    caixa[k] = bons[k][:3]
for a, b in zip(ks, ks[1:]):
    if 1 < b - a <= GAP:
        va, vb = bons[a], bons[b]
        if abs(va[0] - vb[0]) < 25 and abs(va[1] - vb[1]) < 25:   # mesmo plano
            for k in range(a + 1, b):
                u = (k - a) / (b - a)
                caixa[k] = [va[i] + (vb[i] - va[i]) * u for i in range(3)]

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)

# cor da faixa: mediana dos pixels escuros da faixa no quadro de referência
cap.set(cv2.CAP_PROP_POS_FRAMES, int(9 * fps))
_, ref = cap.read()
reg = ref[470:486, 176:266].reshape(-1, 3)
esc = reg[reg.sum(1) < np.percentile(reg.sum(1), 55)]
COR = tuple(int(c) for c in np.median(esc, 0)[::-1])   # RGB
print("cor da faixa (RGB):", COR, "| quadros com remendo:", len(caixa))


def remendo(w, h):
    pad_x, pad_y = int(w * 0.04), int(h * 0.18)
    W2, H2 = w + 2 * pad_x, h + 2 * pad_y
    im = Image.new("RGBA", (W2, H2), COR + (255,))
    d = ImageDraw.Draw(im)
    txt = "LYMPHORIA"

    def largura(f, esp):
        return sum(d.textlength(c, font=f) for c in txt) + esp * (len(txt) - 1)

    tam = max(8, int(h * 0.60))
    f = ImageFont.truetype(str(FONTE), tam)
    esp = tam * 0.18
    while largura(f, esp) > W2 * 0.82 and tam > 8:
        tam -= 1
        f = ImageFont.truetype(str(FONTE), tam)
        esp = tam * 0.18
    bb = d.textbbox((0, 0), "LYMPHORIA", font=f)
    x = (W2 - largura(f, esp)) / 2
    y = (H2 - (bb[3] - bb[1])) / 2 - bb[1]
    for c in txt:
        d.text((x, y), c, font=f, fill=(240, 242, 238, 255))
        x += d.textlength(c, font=f) + esp
    im = im.filter(ImageFilter.GaussianBlur(1.1))             # casa com a maciez do 360p ampliado
    mask = Image.new("L", (W2, H2), 0)
    ImageDraw.Draw(mask).rectangle([2, 2, W2 - 3, H2 - 3], fill=255)
    im.putalpha(mask.filter(ImageFilter.GaussianBlur(2)))
    return im, pad_x, pad_y


def processa(i, frame):
    big = cv2.resize(frame, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    if i in caixa:
        x, y, s = caixa[i]
        w, h = int(TW * s * ESC), int(TH * s * ESC)
        pim, px, py = remendo(w, h)
        base = Image.fromarray(cv2.cvtColor(big, cv2.COLOR_BGR2RGB)).convert("RGBA")
        base.alpha_composite(pim, (max(0, int(x * ESC) - px), max(0, int(y * ESC) - py)))
        novo = cv2.cvtColor(np.array(base.convert("RGB")), cv2.COLOR_RGB2BGR)
        # legenda queimada (branco puro + contorno) passa por cima do remendo
        leg = (big.min(2) > 232).astype(np.uint8)
        leg = cv2.dilate(leg, np.ones((7, 7), np.uint8)).astype(bool)
        novo[leg] = big[leg]
        big = novo
    return big


if preview:
    for t in preview:
        i = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, fr = cap.read()
        cv2.imwrite(str(Path(saida).with_name(f"prev_{t:05.2f}.jpg")), processa(i, fr))
    sys.exit(0)

n_fim = int(round(corte * fps))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920",
                       "-r", str(fps), "-i", "-", "-ss", "0", "-t", f"{corte:.3f}", "-i", src,
                       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                       "-af", f"afade=t=out:st={corte - 0.12:.3f}:d=0.12", "-shortest", saida], stdin=subprocess.PIPE)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
for i in range(n_fim):
    ok, fr = cap.read()
    if not ok:
        break
    ff.stdin.write(processa(i, fr).tobytes())
ff.stdin.close()
ff.wait()
print("ok:", saida, "quadros:", n_fim)

# -*- coding: utf-8 -*-
"""Troca um texto plano que se move pouco (ex.: marca no cabeçalho de uma tela de celular) acompanhando o
movimento: rastreia a caixa quadro a quadro (template matching), apaga as letras claras e escreve o texto novo.

  python remendo_rastreado.py entrada.mp4 saida.mp4 --caixa x0,y0,x1,y1 --texto LYMPHORIA [--ref 0.3]
       [--fonte Poppins-Medium.ttf] [--cor-texto 255,255,255] [--espaco 0.12]
Sem áudio na saída (use em clipes de take). A caixa é medida no quadro --ref.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTS = Path(__file__).resolve().parent.parent / "fonts"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--caixa", required=True)
    ap.add_argument("--texto", required=True)
    ap.add_argument("--ref", type=float, default=0.0)
    ap.add_argument("--fonte", default="Poppins-Medium.ttf")
    ap.add_argument("--cor-texto", default="255,255,255")
    ap.add_argument("--espaco", type=float, default=0.12)
    a = ap.parse_args()
    x0, y0, x1, y1 = map(int, a.caixa.split(","))
    w, h = x1 - x0, y1 - y0
    cap = cv2.VideoCapture(a.entrada)
    fps = cap.get(cv2.CAP_PROP_FPS)
    W, H = int(cap.get(3)), int(cap.get(4))
    quadros = []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        quadros.append(im)
    ref = quadros[min(len(quadros) - 1, int(round(a.ref * fps)))]
    tpl = cv2.cvtColor(ref[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    cor_txt = tuple(int(c) for c in a.cor_texto.split(","))
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fps}", "-i", "-", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", a.saida],
                          stdin=subprocess.PIPE)
    px, py = x0, y0
    for im in quadros:
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        sx0, sy0 = max(0, px - 40), max(0, py - 40)
        janela = g[sy0:min(H, py + h + 40), sx0:min(W, px + w + 40)]
        r = cv2.matchTemplate(janela, tpl, cv2.TM_CCOEFF_NORMED)
        _, sc, _, loc = cv2.minMaxLoc(r)
        if sc > 0.4:
            px, py = sx0 + loc[0], sy0 + loc[1]
        reg = im[py:py + h, px:px + w]
        letras = (reg.min(2) > 170).astype(np.uint8)
        m = np.zeros(im.shape[:2], np.uint8)
        m[py:py + h, px:px + w] = cv2.dilate(letras, np.ones((5, 5), np.uint8))
        im = cv2.inpaint(im, m, 5, cv2.INPAINT_TELEA)
        pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(pil)
        tam = int(h * 0.62)
        f = ImageFont.truetype(str(FONTS / a.fonte), tam)
        esp = tam * a.espaco
        larg = sum(d.textlength(c, font=f) for c in a.texto) + esp * (len(a.texto) - 1)
        while larg > w * 0.95 and tam > 6:
            tam -= 1
            f = ImageFont.truetype(str(FONTS / a.fonte), tam)
            esp = tam * a.espaco
            larg = sum(d.textlength(c, font=f) for c in a.texto) + esp * (len(a.texto) - 1)
        bb = d.textbbox((0, 0), a.texto, font=f)
        x = px + (w - larg) / 2
        y = py + (h - (bb[3] - bb[1])) / 2 - bb[1]
        for c in a.texto:
            d.text((x, y), c, font=f, fill=cor_txt)
            x += d.textlength(c, font=f) + esp
        ff.stdin.write(cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR).tobytes())
    ff.stdin.close()
    ff.wait()
    print(f"ok: {a.saida} | {len(quadros)} quadros")


if __name__ == "__main__":
    main()

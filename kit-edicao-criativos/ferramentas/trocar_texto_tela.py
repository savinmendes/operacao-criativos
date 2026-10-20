# -*- coding: utf-8 -*-
"""Troca um texto queimado na tela (ex.: nome de marca na legenda) por outro, num intervalo de tempo.
Apaga as letras brancas (e o contorno) dentro da caixa e escreve o texto novo centralizado, branco
com contorno preto (Poppins Bold do kit), no mesmo tamanho aproximado.

  python trocar_texto_tela.py entrada.mp4 saida.mp4 --de 181.47 --ate 183.43 \
      --caixa 312,1410,765,1467 --texto "Lymphoria, 4" [--px 58] [--contorno 5]
Áudio é copiado sem mexer. Só os quadros do intervalo são reprocessados.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONTE = Path(__file__).resolve().parent.parent / "fonts" / "Poppins-Bold.ttf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--de", type=float, required=True)
    ap.add_argument("--ate", type=float, required=True)
    ap.add_argument("--caixa", required=True, help="x0,y0,x1,y1 em px do vídeo")
    ap.add_argument("--texto", required=True)
    ap.add_argument("--px", type=int, default=0, help="tamanho da fonte; 0 = altura da caixa x 0,82")
    ap.add_argument("--contorno", type=int, default=5)
    ap.add_argument("--fonte", default="Poppins-Bold.ttf", help="arquivo em kit/fonts (ex.: Poppins-Medium.ttf)")
    ap.add_argument("--ref", type=float, default=None,
                    help="instante em que o texto antigo está na tela; só troca quadros com o MESMO texto (janela --de/--ate)")
    ap.add_argument("--maiusc", action="store_true", help="escreve o texto em MAIÚSCULAS")
    a = ap.parse_args()
    if a.maiusc:
        a.texto = a.texto.upper()
    global FONTE
    FONTE = FONTE.parent / a.fonte
    x0, y0, x1, y1 = map(int, a.caixa.split(","))
    cap = cv2.VideoCapture(a.entrada)
    fps = cap.get(cv2.CAP_PROP_FPS)
    W, H = int(cap.get(3)), int(cap.get(4))
    i0, i1 = int(round(a.de * fps)), int(round(a.ate * fps))
    px = a.px or int((y1 - y0) * 0.82)
    ref_mask = None
    if a.ref is not None:
        cr = cv2.VideoCapture(a.entrada)
        cr.set(cv2.CAP_PROP_POS_FRAMES, int(round(a.ref * fps)))
        _, rim = cr.read()
        ref_mask = rim[y0:y1, x0:x1].min(2) > 200
    fonte = ImageFont.truetype(str(FONTE), px)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fps}", "-i", "-", "-i", a.entrada, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                           "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", a.saida],
                          stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        mesmo = True
        if i0 <= i <= i1 and ref_mask is not None:
            cur = im[y0:y1, x0:x1].min(2) > 200
            mesmo = (cur & ref_mask).sum() / max(1, ref_mask.sum()) > 0.6
        if i0 <= i <= i1 and mesmo:
            reg = im[y0:y1, x0:x1]
            letras = (reg.min(2) > 200).astype(np.uint8)
            m = np.zeros(im.shape[:2], np.uint8)
            m[y0:y1, x0:x1] = cv2.dilate(letras, np.ones((2 * a.contorno + 3,) * 2, np.uint8))
            im = cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)
            pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            d = ImageDraw.Draw(pil)
            bb = d.textbbox((0, 0), a.texto, font=fonte, stroke_width=a.contorno)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), a.texto, font=fonte,
                   fill=(255, 255, 255), stroke_width=a.contorno, stroke_fill=(0, 0, 0))
            im = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        ff.stdin.write(im.tobytes())
        i += 1
    ff.stdin.close()
    ff.wait()
    print(f"ok: {a.saida} | {i1 - i0 + 1} quadros com texto trocado")


if __name__ == "__main__":
    main()

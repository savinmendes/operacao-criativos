# -*- coding: utf-8 -*-
"""Gera folhas de contato (1 quadro a cada N s, com o tempo escrito) para revisar vídeos rapidamente.
Mostra progresso e tempo restante estimado.

  python folhas_contato.py --cada 3 --saida pasta video1.mp4 video2.mp4 ...
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2
import numpy as np


def fmt(s):
    s = int(max(0, s))
    return f"{s // 60}min{s % 60:02d}s" if s >= 60 else f"{s}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cada", type=float, default=3.0)
    ap.add_argument("--colunas", type=int, default=12)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--de", type=float, default=0.0, help="começa neste segundo (tempo real escrito no quadro)")
    ap.add_argument("--ate", type=float, default=None, help="termina neste segundo")
    ap.add_argument("--largura", type=int, default=150)
    ap.add_argument("videos", nargs="+")
    a = ap.parse_args()
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    durs = []
    for v in a.videos:
        c = cv2.VideoCapture(v)
        durs.append(c.get(cv2.CAP_PROP_FRAME_COUNT) / (c.get(cv2.CAP_PROP_FPS) or 30))
    total, feito, t0 = sum(durs), 0.0, time.time()
    for k, (v, d) in enumerate(zip(a.videos, durs), 1):
        cap = cv2.VideoCapture(v)
        ims, t = [], a.de
        fim = min(d, a.ate) if a.ate else d
        while t < fim:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, im = cap.read()
            if not ok:
                break
            im = cv2.resize(im, (a.largura, int(a.largura * 16 / 9)))
            cv2.rectangle(im, (0, 0), (62, 20), (0, 0, 0), -1)
            cv2.putText(im, f"{int(t // 60)}:{int(t % 60):02d}", (3, 15), 0, 0.5, (0, 255, 255), 1)
            ims.append(im)
            t += a.cada
        while len(ims) % a.colunas:
            ims.append(np.zeros_like(ims[0]))
        linhas = [np.hstack(ims[i:i + a.colunas]) for i in range(0, len(ims), a.colunas)]
        # quebra em folhas de no máx. 8 linhas
        for p in range(0, len(linhas), 8):
            cv2.imwrite(str(out / f"{Path(v).stem}_folha{p // 8 + 1}.jpg"), np.vstack(linhas[p:p + 8]),
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
        feito += d
        dec = time.time() - t0
        resta = dec / feito * (total - feito) if feito else 0
        print(f"[{k}/{len(a.videos)}] {Path(v).name} ({fmt(d)} de vídeo) | {feito / total:.0%} | "
              f"decorrido {fmt(dec)} | falta ~{fmt(resta)}", flush=True)


if __name__ == "__main__":
    main()

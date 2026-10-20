# -*- coding: utf-8 -*-
"""Encaixa um take editado por IA (ex.: Kling O1 Edit, que devolve 24 fps e duração levemente diferente)
de volta no tempo do take original, quadro a quadro, e restaura por cima a legenda queimada original.

  python encaixar_edit.py original.mp4 editado.mp4 saida.mp4 [--dur 2.6] [--sem-legenda]

- Para cada quadro do original acha o quadro editado mais parecido (busca monotônica numa janela),
  então o movimento e a legenda queimada voltam a bater com o áudio.
- Legenda queimada (texto branco puro + contorno) do original é copiada por cima do quadro editado,
  porque a IA costuma redesenhar o texto com letras erradas.
- --dur: usa só os primeiros N s (takes que foram estendidos em vai-e-volta antes da edição).
Saída sem áudio, 30 fps, mesma resolução do original.
"""
from __future__ import annotations

import argparse
import subprocess

import cv2
import numpy as np


def ler(p):
    c = cv2.VideoCapture(p)
    fps = c.get(cv2.CAP_PROP_FPS)
    q = []
    while True:
        ok, im = c.read()
        if not ok:
            break
        q.append(im)
    return q, fps


def assinatura(im):
    g = cv2.cvtColor(cv2.resize(im, (72, 128), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    return g.astype(np.float32)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original")
    ap.add_argument("editado")
    ap.add_argument("saida")
    ap.add_argument("--dur", type=float, default=None)
    ap.add_argument("--sem-legenda", action="store_true")
    a = ap.parse_args()

    org, fps_o = ler(a.original)
    edt, fps_e = ler(a.editado)
    if a.dur:
        org = org[:int(round(a.dur * fps_o))]
    H, W = org[0].shape[:2]
    edt = [cv2.resize(e, (W, H), interpolation=cv2.INTER_LANCZOS4) if e.shape[:2] != (H, W) else e for e in edt]
    so, se = [assinatura(x) for x in org], [assinatura(x) for x in edt]

    # alinhamento monotônico: parte da proporção de tempo e procura na vizinhança
    mapa, prev = [], 0
    for i, s in enumerate(so):
        guia = int(round(i / fps_o * fps_e))
        lo, hi = max(prev, guia - 6), min(len(se) - 1, guia + 6)
        if lo > hi:
            lo = hi = min(len(se) - 1, prev)
        j = min(range(lo, hi + 1), key=lambda k: float(np.mean(np.abs(se[k] - s))))
        mapa.append(j)
        prev = j

    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fps_o}", "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                           "-pix_fmt", "yuv420p", a.saida], stdin=subprocess.PIPE)
    k7 = np.ones((7, 7), np.uint8)
    y0, y1 = int(H * 0.62), int(H * 0.90)          # faixa onde a legenda queimada aparece
    alt_min = int(H * 0.018)                        # letra de legenda (~35 px em 1920) >> letra de rótulo

    def letras_grandes(im):
        """máscara das letras brancas grandes (legenda) na faixa, com o contorno preto."""
        m = np.zeros(im.shape[:2], np.uint8)
        b = (im[y0:y1].min(2) > 238).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
        for k in range(1, n):
            x, y, w, h, area = st[k]
            if h >= alt_min and area >= 60 and w < W * 0.25:
                m[y0:y1][lab == k] = 1
        return cv2.dilate(m, np.ones((11, 11), np.uint8))

    for i, j in enumerate(mapa):
        q = edt[j].copy()
        if not a.sem_legenda:
            o = org[i]
            fantasma = letras_grandes(q)                 # legenda redesenhada pela IA
            if fantasma.any():
                # onde o fundo do original = fundo do editado (fora do produto trocado), copia o original;
                # só onde o produto mudou (diferença grande na vizinhança) usa preenchimento automático
                legs = fantasma | letras_grandes(o)
                d = np.abs(q.astype(np.int16) - o.astype(np.int16)).mean(2).astype(np.float32)
                d[legs.astype(bool)] = 0
                peso = cv2.blur((1 - legs).astype(np.float32), (41, 41)) + 1e-3
                viz = cv2.blur(d, (41, 41)) / peso
                igual = (viz < 45) & fantasma.astype(bool)
                q[igual] = o[igual]
                resto = (fantasma.astype(bool) & ~igual).astype(np.uint8)
                if resto.any():
                    q = cv2.inpaint(q, resto, 5, cv2.INPAINT_TELEA)
            leg = cv2.dilate((o.min(2) > 232).astype(np.uint8), k7).astype(bool)
            leg[:y0] = False; leg[y1:] = False   # só a faixa da legenda: fora dela o texto branco é do rótulo (bug corrigido 05/10/2026)
            q[leg] = o[leg]
        ff.stdin.write(q.tobytes())
    ff.stdin.close()
    ff.wait()
    saltos = sum(1 for x, y in zip(mapa, mapa[1:]) if y - x > 2)
    print(f"ok: {a.saida} | {len(mapa)} quadros | editado tinha {len(edt)} @ {fps_e:.0f} fps | saltos>2: {saltos}")


if __name__ == "__main__":
    main()

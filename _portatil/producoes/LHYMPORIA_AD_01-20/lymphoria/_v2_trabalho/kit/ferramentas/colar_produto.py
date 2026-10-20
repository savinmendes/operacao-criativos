# -*- coding: utf-8 -*-
"""Cola SÓ o produto de um take editado por IA sobre o take original (quando a IA trocou o produto
mas também mexeu no personagem/fundo). Mantém tudo do original fora da silhueta do frasco.

  python colar_produto.py original.mp4 editado.mp4 saida.mp4 [--dur 1.33] [--debug quadro.jpg]

Silhueta = fecho convexo das partes "de frasco" (vidro âmbar, faixa verde, tampa preta) no editado
e no original (união, para cobrir também o frasco antigo). Bordas suavizadas; legenda queimada
original restaurada por cima. Saída sem áudio, 30 fps.
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


def partes_frasco(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    ambar = (h >= 3) & (h <= 22) & (s > 110) & (v > 35) & (v < 235)
    verde = (h >= 60) & (h <= 100) & (s > 50) & (v < 140)
    m = (ambar | verde).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return m


def silhueta(im, ref_centro=None):
    m = partes_frasco(im)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        return np.zeros(m.shape, np.uint8), None
    # maior blob (perto do centro anterior, se houver) + vizinhos próximos
    cand = sorted(range(1, n), key=lambda k: -st[k, 4])
    k0 = cand[0]
    if ref_centro is not None:
        k0 = min(cand[:5], key=lambda k: np.hypot(*(cen[k] - ref_centro)) - st[k, 4] * 0.002)
    x, y, w, hh, _ = st[k0]
    sel = np.zeros(m.shape, np.uint8)
    for k in range(1, n):
        cx, cy = cen[k]
        if st[k, 4] > 80 and x - w * 0.6 <= cx <= x + w * 1.6 and y - hh * 1.2 <= cy <= y + hh * 3.0:
            sel[lab == k] = 1
    pts = cv2.findNonZero(sel)
    hull = np.zeros(m.shape, np.uint8)
    cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
    return hull, cen[k0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original")
    ap.add_argument("editado")
    ap.add_argument("saida")
    ap.add_argument("--dur", type=float, default=None)
    ap.add_argument("--debug", default=None)
    a = ap.parse_args()
    org, fo = ler(a.original)
    edt, fe = ler(a.editado)
    if a.dur:
        org = org[:int(round(a.dur * fo))]
    H, W = org[0].shape[:2]
    edt = [cv2.resize(e, (W, H)) if e.shape[:2] != (H, W) else e for e in edt]

    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                           "-r", f"{fo}", "-i", "-", "-c:v", "libx264", "-threads", "4", "-crf", "15", "-pix_fmt", "yuv420p", a.saida],
                          stdin=subprocess.PIPE)
    c_o = c_e = None
    k7 = np.ones((7, 7), np.uint8)
    dbg = []
    for i, o in enumerate(org):
        e = edt[min(len(edt) - 1, int(round(i / fo * fe)))]
        so, c_o = silhueta(o, c_o)
        se, c_e = silhueta(e, c_e)
        m = cv2.dilate(so | se, np.ones((15, 15), np.uint8)).astype(np.float32)
        m = cv2.GaussianBlur(m, (21, 21), 0)[..., None]
        q = (e * m + o * (1 - m)).astype(np.uint8)
        leg = cv2.dilate((o.min(2) > 232).astype(np.uint8), k7).astype(bool)
        # legenda só fora do frasco novo não precisa; dentro dele restaura a do original também
        q[leg] = o[leg]
        ff.stdin.write(q.tobytes())
        if a.debug and i in (0, len(org) // 2, len(org) - 1):
            dbg.append(np.hstack([o, e, q]))
    ff.stdin.close()
    ff.wait()
    if dbg:
        cv2.imwrite(a.debug, cv2.resize(np.vstack(dbg), None, fx=0.25, fy=0.25))
    print(f"ok: {a.saida} | {len(org)} quadros")


if __name__ == "__main__":
    main()

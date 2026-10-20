# -*- coding: utf-8 -*-
"""Restaura a legenda em CAIXA (retângulo branco com texto verde) do take original sobre o take editado pelo Kling.
Por quadro: acha no original o maior retângulo quase branco na faixa y0..y1 e cola esse retângulo (com 3 px de margem).
  python colar_caixa_legenda.py orig.mp4 editado_alinhado.mp4 saida.mp4 [--y0 760 --y1 1100]"""
import argparse, subprocess
import cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("orig"); ap.add_argument("ed"); ap.add_argument("out")
ap.add_argument("--y0", type=int, default=760); ap.add_argument("--y1", type=int, default=1100); a = ap.parse_args()
co, ce = cv2.VideoCapture(a.orig), cv2.VideoCapture(a.ed)
fps = ce.get(cv2.CAP_PROP_FPS) or 30
w, h = int(ce.get(3)), int(ce.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
n = k = 0
while True:
    ok1, fo = co.read(); ok2, fe = ce.read()
    if not ok2: break
    if ok1:
        band = fo[a.y0:a.y1]
        m = (band.min(axis=2) > 215).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        nl, lab, st, _ = cv2.connectedComponentsWithStats(m)
        best = None
        for i in range(1, nl):
            x, y, bw, bh, ar = st[i]
            if ar > 3000 and 40 <= bh <= 140 and bw > 1.5 * bh and ar > 0.6 * bw * bh:
                if best is None or ar > best[4]: best = st[i]
        if best is not None:
            x, y, bw, bh, _ = best; y += a.y0
            x0, y0, x1, y1 = max(0, x - 3), max(0, y - 3), min(w, x + bw + 3), min(h, y + bh + 3)
            fe[y0:y1, x0:x1] = fo[y0:y1, x0:x1]; k += 1
    p.stdin.write(fe.tobytes()); n += 1
p.stdin.close(); p.wait()
print(f"ok {a.out} | {n} quadros, caixa colada em {k}")

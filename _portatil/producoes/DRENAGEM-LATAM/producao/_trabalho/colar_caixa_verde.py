# -*- coding: utf-8 -*-
"""Igual a colar_caixa_legenda.py, mas acha a caixa pelo TEXTO VERDE da legenda (não confunde com rótulo branco).
  python colar_caixa_verde.py orig.mp4 editado_alinhado.mp4 saida.mp4"""
import subprocess, sys
import cv2, numpy as np
orig, ed, out = sys.argv[1:4]
Y0, Y1 = 700, 1150
co, ce = cv2.VideoCapture(orig), cv2.VideoCapture(ed)
w, h = int(ce.get(3)), int(ce.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
n = k = 0
while True:
    ok1, fo = co.read(); ok2, fe = ce.read()
    if not ok2: break
    if ok1:
        b = fo[Y0:Y1].astype(int); B, G, R = b[..., 0], b[..., 1], b[..., 2]
        m = (G > 100) & (G - R > 50) & (G - B > 40)
        rows = np.where(m.sum(1) > 6)[0]
        if len(rows):
            grupos = np.split(rows, np.where(np.diff(rows) > 4)[0] + 1)
            g = max(grupos, key=len)
            if 15 <= g[-1] - g[0] <= 80:
                cols = np.where(m[g[0]:g[-1] + 1].any(0))[0]
                x0, x1 = max(0, cols[0] - 10), min(w, cols[-1] + 11)
                y0, y1 = Y0 + g[0] - 9, Y0 + g[-1] + 10
                borda = np.concatenate([fo[y0:y1, x0:x0 + 4].reshape(-1, 3), fo[y0:y1, x1 - 4:x1].reshape(-1, 3)])
                if m.sum() > 300:
                    fe[y0:y1, x0:x1] = fo[y0:y1, x0:x1]; k += 1
    p.stdin.write(fe.tobytes()); n += 1
p.stdin.close(); p.wait()
print(f"ok {out} | {n} quadros, caixa colada em {k}")

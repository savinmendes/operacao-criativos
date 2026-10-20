# -*- coding: utf-8 -*-
"""Desfoque que acompanha um objeto (caixa interpolada entre quadros-chave).
  python blur_movel.py entrada.mp4 saida.mp4 blur.json
blur.json: [{"chaves":[[t,"x0,y0,x1,y1"],[t,"..."]]}, ...]  (fora do intervalo das chaves nada muda)"""
import json
import subprocess
import sys

import cv2
import numpy as np

ent, sai = sys.argv[1], sys.argv[2]
B = json.load(open(sys.argv[3], encoding="utf-8-sig"))
for b in B:
    b["k"] = [(float(t), np.array(list(map(float, c.split(","))))) for t, c in b["chaves"]]
cap = cv2.VideoCapture(ent)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", sai], stdin=subprocess.PIPE)
i = n = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    t = i / fps
    for b in B:
        k = b["k"]
        if not (k[0][0] <= t <= k[-1][0]):
            continue
        for (ta, ca), (tb, cb) in zip(k, k[1:]):
            if ta <= t <= tb:
                c = ca + (cb - ca) * ((t - ta) / max(1e-6, tb - ta))
                break
        x0, y0, x1, y1 = [int(v) for v in c]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        orig = im.copy()
        reg = im[y0:y1, x0:x1]
        bl = cv2.GaussianBlur(cv2.resize(reg, None, fx=0.15, fy=0.15), (0, 0), 3)
        bl = cv2.resize(bl, (x1 - x0, y1 - y0))
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        cv2.ellipse(m, ((x1 - x0) // 2, (y1 - y0) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
        im[y0:y1, x0:x1] = (bl * m + reg * (1 - m)).astype(np.uint8)
        if b.get("proteger"):  # devolve a legenda (caixa branca + texto azul) que estiver por cima
            px0, py0, px1, py1 = map(int, b["proteger"].split(","))
            o = orig[py0:py1, px0:px1].astype(int)
            leg = (o.min(2) > 200) | ((o[..., 0] > o[..., 2] + 40) & (o.max(2) < 170))
            leg = cv2.morphologyEx(leg.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)).astype(bool)
            im[py0:py1, px0:px1][leg] = orig[py0:py1, px0:px1][leg]
        n += 1
    ff.stdin.write(im.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print(f"ok: {sai} | {n} desfoques")

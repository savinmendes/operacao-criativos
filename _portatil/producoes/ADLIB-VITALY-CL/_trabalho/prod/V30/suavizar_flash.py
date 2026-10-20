# -*- coding: utf-8 -*-
"""Frames 162-169 (flash laranja): mistura gradual do último quadro Kling (161) com o flash, para não virar corte duro."""
import subprocess, cv2, numpy as np
c = cv2.VideoCapture("parte1.mp4"); Q = []
while True:
    ok, im = c.read()
    if not ok: break
    Q.append(im)
k = Q[161].astype(np.float32)
for j, f in enumerate(range(162, 170)):
    a = (j + 1) / 9.0
    fl = Q[f].astype(np.float32)
    # leva o tom do flash para o quadro Kling e mistura
    tint = k * (fl.mean((0, 1)) / np.maximum(k.mean((0, 1)), 1))
    Q[f] = np.clip(tint * (1 - a) + fl * a, 0, 255).astype(np.uint8)
H, W = Q[0].shape[:2]
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-i", "parte1.mp4", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p",
                       "-c:a", "copy", "parte1b.mp4"], stdin=subprocess.PIPE)
for q in Q: ff.stdin.write(q.tobytes())
ff.stdin.close(); ff.wait(); print("ok", len(Q))

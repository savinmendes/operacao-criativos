# -*- coding: utf-8 -*-
"""Desfoque forte (mosaico 6% + gaussiano) numa caixa com borda suave, de quadro i0 a i1.
  python blur_forte.py in.mp4 out.mp4 i0 i1 x0,y0,x1,y1"""
import subprocess, sys, cv2, numpy as np
ent, sai, i0, i1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
x0, y0, x1, y1 = map(int, sys.argv[5].split(","))
cap = cv2.VideoCapture(ent); fps = cap.get(5); W, H = int(cap.get(3)), int(cap.get(4))
m = np.zeros((H, W), np.float32); m[y0:y1, x0:x1] = 1; m = cv2.GaussianBlur(m, (0, 0), 12)[..., None]
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                       "-pix_fmt", "yuv420p", "-c:a", "copy", "-threads", "3", sai], stdin=subprocess.PIPE)
i = 0
while True:
    ok, im = cap.read()
    if not ok: break
    if i0 <= i <= i1:
        r = im[y0:y1, x0:x1]
        s = cv2.resize(r, None, fx=0.06, fy=0.06, interpolation=cv2.INTER_AREA)
        s = cv2.GaussianBlur(cv2.resize(s, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR), (0, 0), 14)
        b = im.copy(); b[y0:y1, x0:x1] = s
        im = (b * m + im * (1 - m)).astype(np.uint8)
    ff.stdin.write(im.tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok", sai)

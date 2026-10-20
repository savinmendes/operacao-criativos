# -*- coding: utf-8 -*-
"""Cola só uma região (retângulo com borda suave) do take editado sobre o original. python comp_regiao.py orig.mp4 edit.mp4 out.mp4 x0,y0,x1,y1"""
import sys, subprocess, cv2, numpy as np
o, e, out, bx = sys.argv[1:5]
x0, y0, x1, y1 = map(int, bx.split(","))
co, ce = cv2.VideoCapture(o), cv2.VideoCapture(e)
W, H = int(co.get(3)), int(co.get(4))
m = np.zeros((H, W), np.float32); m[y0:y1, x0:x1] = 1
m = cv2.GaussianBlur(m, (0, 0), 12)[..., None]
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
n = 0
while True:
    a, fo = co.read(); b, fe = ce.read()
    if not (a and b): break
    ff.stdin.write((fe * m + fo * (1 - m)).astype(np.uint8).tobytes()); n += 1
ff.stdin.close(); ff.wait(); print("ok", n)

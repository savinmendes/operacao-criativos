# -*- coding: utf-8 -*-
"""Cola só a região do frasco (caixa interpolada entre chaves, borda suave) do take editado sobre o original.
python comp_movel.py orig.mp4 edit.mp4 out.mp4 "t:x0,y0,x1,y1" ..."""
import sys, subprocess, cv2, numpy as np
o, e, out = sys.argv[1:4]
K = [(float(s.split(":")[0]), np.array(list(map(float, s.split(":")[1].split(","))))) for s in sys.argv[4:]]
co, ce = cv2.VideoCapture(o), cv2.VideoCapture(e)
W, H = int(co.get(3)), int(co.get(4))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
i = 0
while True:
    a, fo = co.read(); b, fe = ce.read()
    if not (a and b): break
    t = i / 30
    if t <= K[0][0]: c = K[0][1]
    elif t >= K[-1][0]: c = K[-1][1]
    else:
        for (ta, ca), (tb, cb) in zip(K, K[1:]):
            if ta <= t <= tb: c = ca + (cb - ca) * (t - ta) / (tb - ta); break
    x0, y0, x1, y1 = [int(v) for v in c]
    m = np.zeros((H, W), np.float32); m[max(0, y0):y1, max(0, x0):x1] = 1
    m = cv2.GaussianBlur(m, (0, 0), 10)[..., None]
    ff.stdin.write((fe * m + fo * (1 - m)).astype(np.uint8).tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok", i)

# -*- coding: utf-8 -*-
"""Desfoca rosto do terceiro e data da tela do app (05, ~17.8-21.95 s) com caixas por keyframe interpoladas.
  python blur_track.py entrada.mp4 saida.mp4"""
import subprocess
import sys

import cv2
import numpy as np

DE, ATE = 17.80, 21.97
# t: (rosto cx, cy), (data cx, cy)   coordenadas 720x1280
KF = [
    (17.75, (345, 145), (530, 468)),
    (17.85, (345, 150), (530, 468)),
    (18.3, (385, 195), (575, 520)),
    (18.8, (433, 235), (595, 542)),
    (19.3, (360, 245), (543, 555)),
    (19.8, (273, 225), (470, 529)),
    (20.3, (330, 165), (544, 464)),
    (20.8, (356, 222), (564, 500)),
    (21.3, (309, 190), (495, 464)),
    (21.85, (368, 277), (592, 538)),
    (21.97, (368, 277), (592, 538)),
]
FW, FH = 190, 190   # caixa do rosto
DW, DH = 230, 70    # caixa da data


def interp(t):
    for a, b in zip(KF, KF[1:]):
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0
            f = [a[1][i] + k * (b[1][i] - a[1][i]) for i in (0, 1)]
            d = [a[2][i] + k * (b[2][i] - a[2][i]) for i in (0, 1)]
            return f, d
    return None


ent, sai = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(ent)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps}",
                       "-i", "-", "-i", ent, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "15", "-threads", "4",
                       "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", sai], stdin=subprocess.PIPE)
i = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    t = i / fps
    r = interp(t) if DE <= t <= ATE else None
    if r:
        mask = np.zeros((H, W), np.float32)
        (fx, fy), (dx, dy) = r
        cv2.ellipse(mask, (int(fx), int(fy)), (FW // 2, FH // 2), 0, 0, 360, 1, -1)
        mask[int(dy - DH / 2):int(dy + DH / 2), int(dx - DW / 2):int(dx + DW / 2)] = 1
        mask = cv2.GaussianBlur(mask, (31, 31), 0)[..., None]
        b = cv2.GaussianBlur(im, (61, 61), 0)
        b = cv2.GaussianBlur(b, (61, 61), 0)
        im = (b * mask + im * (1 - mask)).astype(np.uint8)
    ff.stdin.write(im.tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print("ok", sai)

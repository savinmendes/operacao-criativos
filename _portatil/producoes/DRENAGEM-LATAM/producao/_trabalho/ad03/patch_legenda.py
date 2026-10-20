# -*- coding: utf-8 -*-
"""Cobre legenda queimada 'velha' (de fala cortada) nas emendas: nos quadros [de, ate) cola por cima a caixa de
legenda do quadro ref (a legenda certa que entra logo depois). Gera leg/LNN.mp4 + leg/extras_leg.json.
Faixa de busca da caixa branca: y 880-1010 (720x1280)."""
import json, subprocess
import cv2, numpy as np
JAN = [(84.70, 85.20, 85.23), (98.90, 99.067, 99.10), (113.267, 113.367, 113.40), (159.267, 159.667, 159.70),
       (199.067, 199.667, 199.70), (252.333, 252.633, 252.67), (269.40, 270.633, 270.67), (322.30, 322.933, 322.97),
       (370.067, 370.667, 370.70), (392.533, 393.467, 393.50), (531.233, 531.533, 531.57), (611.60, 611.933, 611.97),
       (640.50, 640.867, 640.90), (439.533, 440.533, 440.57), (578.60, 579.433, 579.47), (138.333, 138.40, 138.30)]
Y0, Y1 = 880, 1010
cap = cv2.VideoCapture('full_up720.mp4')
def quadro(n):
    cap.set(cv2.CAP_PROP_POS_FRAMES, n); return cap.read()[1]
def caixa(f):
    h = cv2.cvtColor(f[Y0:Y1], cv2.COLOR_BGR2HSV)
    m = ((h[..., 2] > 235) & (h[..., 1] < 25)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if k < 2: return None
    i = 1 + int(np.argmax(st[1:, 4])); x, y, w, hh, a = st[i]
    return (x, y + Y0, x + w, y + Y0 + hh) if a > 800 else None
ext = []
for j, (de, ate, ref) in enumerate(JAN, 1):
    n0, n1, nr = round(de * 30), round(ate * 30), round(ref * 30)
    R = quadro(nr); br = caixa(R)
    W, H = R.shape[1], R.shape[0]
    out = f'leg/L{j:02d}.mp4'
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        f = quadro(n); b = caixa(f)
        bs = [v for v in (b, br) if v]
        x0 = max(0, min(v[0] for v in bs) - 8); y0 = max(0, min(v[1] for v in bs) - 8)
        x1 = min(W, max(v[2] for v in bs) + 8); y1 = min(H, max(v[3] for v in bs) + 8)
        m = np.zeros((H, W), np.float32); m[y0:y1, x0:x1] = 1
        m = cv2.GaussianBlur(m, (9, 9), 0)[..., None]
        f = (R * m + f * (1 - m)).astype(np.uint8)
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    ext.append({"clipe": out, "inicio": round(n0 / 30, 4), "quadros": n1 - n0})
    print(j, de, ate, 'caixa ref', br)
json.dump(ext, open('leg/extras_leg.json', 'w'), indent=1)

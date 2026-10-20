# -*- coding: utf-8 -*-
"""Cola a saída do HeyGen (recorte escalado p/ 720x1280) de volta na base, só numa elipse suave na parte de baixo do
rosto da Desatadora (boca/queixo), fora do canto do Jesus. Reamostra no tempo (interpolação) para N quadros."""
import json, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent
ROS = json.loads((AQ / "rostos.json").read_text())
def ler(p, ini=0, n=None):
    cap = cv2.VideoCapture(str(p)); fr = []; k = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        if k >= ini: fr.append(f)
        k += 1
        if n and len(fr) >= n: break
    return fr
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / max(1, n - 1); j = int(np.floor(x)); a = x - j
        if j >= m - 1: out.append(fr[-1]); continue
        out.append(fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0))
    return out
def mascara(nome, canto):
    x0, y0, x1, y1 = ROS[nome]["w"]
    cx = (x0 + x1) / 2; cy = y0 + 0.62 * (y1 - y0)
    ax = (x1 - x0) / 2 + 6; ay = 0.45 * (y1 - y0) + 10
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(cx), int(cy)), (int(ax), int(ay)), 0, 0, 360, 1.0, -1)
    if canto: m[:canto[1], :canto[0]] = 0
    m = cv2.GaussianBlur(m, (0, 0), 9)
    return m[..., None]
def colador(nome, caixa, canto):
    X0, Y0, W, H = caixa; M = mascara(nome, canto)
    def colar(base, g):
        c = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)
        full = base.copy(); full[Y0:Y0+H, X0:X0+W] = c
        return np.clip(full * M + base * (1 - M), 0, 255).astype(np.uint8)
    return colar

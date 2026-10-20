# -*- coding: utf-8 -*-
"""Cola a saida do HeyGen (recorte 720x1280 = 2,5x do recorte 288x512 em (318,196)) de volta na base limpa,
so na regiao do rosto/boca, com borda suave. Reamostra no tempo para o numero exato de quadros (sem congelar).
Funcoes usadas por medir_out.py e recolocar2.py."""
import cv2, numpy as np
X0, Y0, W, H = 318, 196, 288, 512
def mascara():
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (425, 468), (90, 88), 0, 0, 360, 1.0, -1)
    m = cv2.GaussianBlur(m, (0, 0), 10)
    return m[..., None]
M = mascara()
def ler(p):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr, n):
    """lista de n quadros: interpolacao linear no tempo (n' != n), sem repetir o ultimo."""
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / (n - 1); j = int(np.floor(x)); a = x - j
        if j >= m - 1: out.append(fr[-1]); continue
        out.append(fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0))
    return out
def colar(base, g):
    c = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)
    full = base.copy(); full[Y0:Y0+H, X0:X0+W] = c
    return np.clip(full * M + base * (1 - M), 0, 255).astype(np.uint8)

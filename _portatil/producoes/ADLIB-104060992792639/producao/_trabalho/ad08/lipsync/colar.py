# -*- coding: utf-8 -*-
"""AD 08: cola a saída do HeyGen (recorte rastreado, escalado p/ 720x1280) de volta na base, quadro a quadro,
só numa elipse suave na boca/queixo da Desatadora (caixa do rosto por quadro em trilhas/sNN.json)."""
import json, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent
def ler(p):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
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
def colar(): pass
def colador(nome):
    T = json.loads((AQ / "trilhas" / f"{nome}.json").read_text())
    W, H = T["W"], T["H"]
    R = np.array(T["rosto"]); cx = (R[:, 0] + R[:, 2]) / 2; cy = (R[:, 1] + R[:, 3]) / 2; fw = np.median(R[:, 2] - R[:, 0])
    # quadros em que a detecção trocou a mulher pelo Jesus (centro longe da mediana): na entrada do HeyGen o rosto dela
    # saiu borrado. Nesses quadros: caixa do rosto interpolada e a boca vem da saída do quadro bom mais próximo.
    ruins = set(np.where((np.abs(cx - np.median(cx)) > 0.4 * fw) | (np.abs(cy - np.median(cy)) > 0.4 * fw))[0].tolist())
    bons = [i for i in range(len(R)) if i not in ruins]
    Rc = np.array([np.interp(range(len(R)), bons, R[bons, j]) for j in range(4)]).T
    colar.ruins = ruins
    def colar_q(base, G, i):
        j = i if i not in ruins else min(bons, key=lambda b: abs(b - i))
        g = G[j]; x0, y0 = T["X0"][j], T["Y0"][j]; r = Rc[i]
        c = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)
        full = base.copy(); full[y0:y0+H, x0:x0+W] = c
        fw, fh = r[2] - r[0], r[3] - r[1]
        m = np.zeros((1280, 720), np.float32)
        cv2.ellipse(m, (int((r[0]+r[2])/2), int(r[1] + 0.68*fh)), (int(0.42*fw + 6), int(0.36*fh + 8)), 0, 0, 360, 1.0, -1)
        m[:y0, :] = 0; m[y0+H:, :] = 0; m[:, :x0] = 0; m[:, x0+W:] = 0
        m = cv2.GaussianBlur(m, (0, 0), max(4, fw / 25))[..., None]
        return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8)
    return colar_q

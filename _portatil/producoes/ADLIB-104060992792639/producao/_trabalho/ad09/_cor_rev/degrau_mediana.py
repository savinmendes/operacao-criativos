# -*- coding: utf-8 -*-
# AD 09 (copia adaptada de _ad1718/degrau_mediana.py): MEDIANA de (video - original) dentro da elipse colada (a mesma do
# lipsync/recolocar.py, encolhida 0,8) x anel de pele fora dela, por trecho; mais rosto e fundo.
# Uso: python degrau_mediana.py arquivo.mp4   (base_lipsync de 24 fps, mesmo tempo do original)
import sys, json, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parents[1] / "lipsync"; T = AQ.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros
arq = Path(sys.argv[1]); CFG = json.loads((AQ / "segs.json").read_text())
seg = {}
for s in CFG["segs"]:
    a, b = s["q"]; bx = json.loads((AQ / "boxes" / f"{s['nome']}.json").read_text())["boxes"]
    for j in range(0, b - a + 1, 4): seg[a + j] = (s["nome"], bx[j]["face"])
mx = max(seg) + 1; F = quadros(arq, 0, mx); O = quadros(T.parents[1] / "UNICOS_HD" / "09.mp4", 0, mx); res = {}
for i in range(mx):
    f, o = next(F), next(O)
    if i not in seg: continue
    nm, (x0, y0, x1, y1) = seg[i]; fw, fh = x1 - x0, y1 - y0; ctr = (int((x0 + x1) / 2), int(y0 + 0.70 * fh)); ax = (0.38 * fw, 0.32 * fh)
    e = np.zeros((1280, 720), np.uint8); cv2.ellipse(e, ctr, (int(ax[0] * 0.8), int(ax[1] * 0.8)), 0, 0, 360, 1, -1)
    r = np.zeros((1280, 720), np.uint8); cv2.ellipse(r, ctr, (int(ax[0] * 1.9), int(ax[1] * 1.9)), 0, 0, 360, 1, -1)
    r2 = np.zeros((1280, 720), np.uint8); cv2.ellipse(r2, ctr, (int(ax[0] * 1.3), int(ax[1] * 1.3)), 0, 0, 360, 1, -1)
    Yf = cv2.cvtColor(f, cv2.COLOR_BGR2YUV).astype(float); Yo = cv2.cvtColor(o, cv2.COLOR_BGR2YUV).astype(float); d = Yf - Yo
    fu = np.ones((1280, 720), bool); fu[max(0, int(y0) - 150):int(y1) + 250, :] = False
    res.setdefault(nm, []).append((np.median(d[..., 0][e > 0]), np.median(d[..., 0][(r > 0) & (r2 == 0)]),
                                   np.median(d[..., 1][(r > 0) & (r2 == 0)]), np.median(d[..., 2][(r > 0) & (r2 == 0)]),
                                   np.median(d[..., 0][fu])))
tot = []
print(f"AD 09 ({arq.name}): mediana video-original (Y) | elipse colada | anel fora (Y U V) | degrau | fundo")
for nm, v in res.items():
    v = np.median(np.array(v), 0); tot.append(v)
    print(f"  {nm:5} {v[0]:+5.1f} | {v[1]:+5.1f} {v[2]:+5.1f} {v[3]:+5.1f} | {v[0]-v[1]:+5.1f} | {v[4]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS {v[0]:+5.1f} | {v[1]:+5.1f} {v[2]:+5.1f} {v[3]:+5.1f} | {v[0]-v[1]:+5.1f} | {v[4]:+5.1f}")

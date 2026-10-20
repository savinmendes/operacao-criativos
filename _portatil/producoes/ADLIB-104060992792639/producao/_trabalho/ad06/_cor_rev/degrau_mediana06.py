# copia adaptada de _ad1718/degrau_mediana.py p/ o AD 06: MEDIANA de (arquivo - original) dentro da elipse colada x anel de
# pele fora dela, por trecho. Elipse = rosto do revisor (loteC/escolha_06.json: cx, cy = labio sup., L = largura do rosto),
# 30 fps do final -> quadro de 24 fps da base. Uso: python degrau_mediana06.py arquivo_24fps.mp4
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
AD = Path(__file__).resolve().parent.parent; arq = sys.argv[1]
esc = json.loads((AD.parent / "revisao" / "loteC" / "escolha_06.json").read_text()); seg = {}
for nm, (a, b, t) in esc.items():
    for j, (q, cx, cy, L) in enumerate(t):
        if j % 4 == 0: seg[int(round(q * 24 / 30))] = (nm, cx, cy, L)
mx = max(seg) + 1; F = quadros(arq, 0, mx); O = quadros(AD.parent.parent.parent / "UNICOS_HD" / "06.mp4", 0, mx); res = {}
for i in range(mx):
    f, o = next(F), next(O)
    if i not in seg: continue
    nm, cx, cy, L = seg[i]; ctr = (int(cx), int(cy + 0.25 * L)); ax = (0.40 * L, 0.42 * L)
    e = np.zeros((1280, 720), np.uint8); cv2.ellipse(e, ctr, (int(ax[0] * 0.8), int(ax[1] * 0.8)), 0, 0, 360, 1, -1)
    r = np.zeros((1280, 720), np.uint8); cv2.ellipse(r, ctr, (int(ax[0] * 1.9), int(ax[1] * 1.9)), 0, 0, 360, 1, -1)
    r2 = np.zeros((1280, 720), np.uint8); cv2.ellipse(r2, ctr, (int(ax[0] * 1.3), int(ax[1] * 1.3)), 0, 0, 360, 1, -1)
    d = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float) - cv2.cvtColor(o, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    res.setdefault(nm, []).append((np.median(d[e > 0]), np.median(d[(r > 0) & (r2 == 0)])))
tot = []
print(f"AD 06 ({Path(arq).name}): mediana arquivo-original | elipse colada | anel fora | degrau")
for nm, v in res.items():
    v = np.median(np.array(v), 0); tot.append(v); print(f"  {nm:5} {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")

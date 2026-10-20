# copia adaptada de _ad1718/degrau_mediana.py p/ o AD 07 (elipse fixa por trecho do colar.py):
# MEDIANA de (base_lipsync - original) em luma Y no miolo da elipse colada x anel fora dela (dentro da caixa, fora do
# canto do Jesus), por trecho. Uso: python degrau_mediana.py [arquivo relativo a ad07, padrao base_lipsync.mp4]
import sys, json, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent
sys.path.insert(0, str(T / "ad13" / "lipsync3")); sys.path.insert(0, str(AQ))
from comum3 import quadros
import colar as C
arq = sys.argv[1] if len(sys.argv) > 1 else "base_lipsync.mp4"
SEGS = json.loads((AD / "segmentos.json").read_text())["segmentos"]
geo = {}
for s in SEGS:
    nome = s["nome"]; X0, Y0, W, H = s["caixa"]; canto = None if nome == "s01" else (342, 575)
    M = C.mascara(nome, canto)[..., 0]; fw = C.ROS[nome]["w"][2] - C.ROS[nome]["w"][0]
    dentro = M > 0.01
    anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.35 * fw) | 1,) * 2)).astype(bool) & ~dentro
    cx = np.zeros_like(anel); cx[Y0 + 3:Y0 + H - 3, X0 + 3:X0 + W - 3] = True; anel &= cx
    if canto: anel[:canto[1] + 6, :canto[0] + 6] = False
    for q in range(s["quadro_ini"], s["quadro_ini"] + s["n"], 4): geo[q] = (nome, M > 0.9, anel)
mx = min(max(geo) + 1, 2147); F = quadros(AD / arq, 0, mx); O = quadros(T.parent.parent / "UNICOS_HD" / "07.mp4", 0, mx); res = {}
for i in range(mx):
    f, o = next(F), next(O)
    if i not in geo: continue
    nm, e, r = geo[i]
    d = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float) - cv2.cvtColor(o, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    res.setdefault(nm, []).append((np.median(d[e]), np.median(d[r])))
tot = []
print(f"AD 07 ({arq}): mediana base-original (Y) | miolo elipse colada | anel fora | degrau")
for nm, v in res.items():
    v = np.median(np.array(v), 0); tot.append(v); print(f"  {nm:5} {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")

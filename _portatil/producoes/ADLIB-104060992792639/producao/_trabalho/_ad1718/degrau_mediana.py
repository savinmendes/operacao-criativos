# degrau robusto ao formato da boca: MEDIANA de (final - original) dentro da elipse colada x anel de pele fora dela,
# por trecho (a mediana ignora o +/- do labio que mudou de lugar; um degrau de cor desloca a mediana inteira).
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
NN, arq = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "base_lipsync.mp4"
T = Path(__file__).resolve().parent.parent; AD = T / f"ad{NN}"; AQ = AD / "lipsync"; CFG = json.loads((AQ / "segs.json").read_text())
seg = {}
for s in CFG["segs"]:
    C = np.load(AQ / s.get("cx", f"caixas_{s['nome']}.npy"))
    for j in range(0, s["b"] - s["a"], 4): seg[s["a"] + j] = (s["nome"], C[min(j, len(C) - 1)])
mx = max(seg) + 1; F = quadros(AD / arq, 0, mx); O = quadros(T.parent.parent / "UNICOS_HD" / f"{NN}.mp4", 0, mx); res = {}
for i in range(mx):
    f, o = next(F), next(O)
    if i not in seg: continue
    nm, c = seg[i]; x0, y0, w, h, cx, cy, fw, fh = c; ctr = (int(cx), int(cy + 0.02 * fh)); ax = (0.40 * fw, 0.30 * fh)
    e = np.zeros((1280, 720), np.uint8); cv2.ellipse(e, ctr, (int(ax[0] * 0.8), int(ax[1] * 0.8)), 0, 0, 360, 1, -1)
    r = np.zeros((1280, 720), np.uint8); cv2.ellipse(r, ctr, (int(ax[0] * 1.9), int(ax[1] * 1.9)), 0, 0, 360, 1, -1)
    r2 = np.zeros((1280, 720), np.uint8); cv2.ellipse(r2, ctr, (int(ax[0] * 1.3), int(ax[1] * 1.3)), 0, 0, 360, 1, -1)
    d = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float) - cv2.cvtColor(o, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    res.setdefault(nm, []).append((np.median(d[e > 0]), np.median(d[(r > 0) & (r2 == 0)])))
tot = []
print(f"AD {NN} ({arq}): mediana final-original | elipse colada | anel fora | degrau")
for nm, v in res.items():
    v = np.median(np.array(v), 0); tot.append(v); print(f"  {nm:5} {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")
v = np.median(np.array(tot), 0); print(f"  TODOS {v[0]:+5.1f} {v[1]:+5.1f} {v[0]-v[1]:+5.1f}")

# decompoe o degrau do cor.py: (colada - base corrigida) e (base corrigida - original) nas caixas boca/face, por trecho
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
NN, esc_dir, segs = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
T = Path(__file__).resolve().parent.parent; AD = T / f"ad{NN}"; AG = np.load(Path(__file__).parent / f"cor_global_{NN}.npy")
fps = json.loads((AD / "lipsync" / "segs.json").read_text())["fps"]
esc = json.loads((esc_dir / f"escolha_{NN}.json").read_text()); pos = {}
for k, (a, b, t) in esc.items():
    if k in segs:
        for q, cx, cy, L in t[::2]: pos[int(round(q / 30 * fps))] = (k, cx, cy, L)
mx = max(pos) + 1
BL = quadros(AD / "base_lipsync.mp4", 0, mx); BS = quadros(AD / "base_sem_legenda.mp4", 0, mx); OR = quadros(T.parent.parent / "UNICOS_HD" / f"{NN}.mp4", 0, mx)
def Y(f): return cv2.cvtColor(f, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
def bx(y, cx, cy, w, h): x0, y0 = int(max(0, cx - w / 2)), int(max(0, cy - h / 2)); return y[y0:int(y0 + h), x0:int(x0 + w)].mean()
res = {}
for i in range(mx):
    bl, bs, o = next(BL), next(BS), next(OR)
    if i not in pos: continue
    k, cx, cy, L = pos[i]
    bc = np.clip(bs.reshape(-1, 3).astype(np.float32) @ AG[:3].astype(np.float32) + AG[3].astype(np.float32) + .5, 0, 255).reshape(bs.shape).astype(np.uint8)
    yl, yc, yo = Y(bl), Y(bc), Y(o)
    def bf(y): return ((bx(y, cx, cy - 0.17 * L, 0.30 * L, 0.08 * L) + bx(y, cx, cy + 0.30 * L, 0.30 * L, 0.12 * L)) / 2,
                       (bx(y, cx - 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L) + bx(y, cx + 0.33 * L, cy - 0.55 * L, 0.14 * L, 0.14 * L)) / 2)
    l, c, oo = bf(yl), bf(yc), bf(yo)
    res.setdefault(k, []).append((l[0] - c[0], c[0] - oo[0], l[1] - c[1], c[1] - oo[1], cx, cy, L))
for k, r in res.items():
    r = np.median(np.array(r), 0)
    print(f"{k}: boca colada-basecorr {r[0]:+.1f} basecorr-orig {r[1]:+.1f} | face colada-basecorr {r[2]:+.1f} basecorr-orig {r[3]:+.1f} | rosto cx {r[4]:.0f} cy {r[5]:.0f} L {r[6]:.0f}")

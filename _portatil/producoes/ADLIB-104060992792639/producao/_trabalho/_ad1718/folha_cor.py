# folha: recorte do rosto, final (base_lipsync) em cima x original embaixo, + mapa de diferenca de luma (cinza=0, +-12)
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
NN, out = sys.argv[1], sys.argv[2]; qs = [int(x) for x in sys.argv[3:]]
T = Path(__file__).resolve().parent.parent; AD = T / f"ad{NN}"
fps = json.loads((AD / "lipsync" / "segs.json").read_text())["fps"]
esc = json.loads((T / "revisao" / "loteC" / f"escolha_{NN}.json").read_text()) if (T / "revisao" / "loteC" / f"escolha_{NN}.json").exists() else json.loads((T / "revisao" / "loteB" / f"escolha_{NN}.json").read_text())
pos = {}
for k, (a, b, t) in esc.items():
    for q, cx, cy, L in t: pos[int(round(q / 30 * fps))] = (cx, cy, L)
mx = max(qs) + 1; BL = quadros(AD / "base_lipsync.mp4", 0, mx); OR = quadros(T.parent.parent / "UNICOS_HD" / f"{NN}.mp4", 0, mx); cols = []
for i in range(mx):
    a, o = next(BL), next(OR)
    if i not in qs: continue
    cx, cy, L = pos.get(i, list(pos.values())[0]); x0, y0 = int(cx - 1.0 * L), int(cy - 1.0 * L); s = int(2 * L)
    ca, co = a[y0:y0 + s, x0:x0 + s], o[y0:y0 + s, x0:x0 + s]
    d = cv2.cvtColor(ca, cv2.COLOR_BGR2GRAY).astype(float) - cv2.cvtColor(co, cv2.COLOR_BGR2GRAY).astype(float)
    dm = cv2.applyColorMap(np.clip(128 + cv2.GaussianBlur(d, (0, 0), 3) * 10, 0, 255).astype(np.uint8), cv2.COLORMAP_JET)
    col = np.vstack([cv2.resize(x, (300, 300)) for x in (ca, co, dm)]); cv2.putText(col, str(i), (5, 25), 0, 0.8, (0, 255, 255), 2); cols.append(col)
cv2.imwrite(out, np.hstack(cols))

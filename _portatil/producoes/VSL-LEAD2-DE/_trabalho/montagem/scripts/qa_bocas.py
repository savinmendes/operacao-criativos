import sys, json, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
FIN = sys.argv[1]; ids = sys.argv[3:]; outp = sys.argv[2]
P = json.load(open(M / "params.json")); F0 = int(round(P["T0"] * 30))
rows = []
for i in ids:
    info = json.load(open(M / "comp" / f"{i}.json")); cx, cy, ax, ay = info["elipse_media"]
    k0 = info["q0"] - F0
    fr = ler(FIN, (k0 + 20 - 0.5) / 30, 8 * 12)[::12]
    tiles = []
    for j, f in enumerate(fr):
        z = f[int(max(0, cy - 2.4 * ay)):int(cy + 2.0 * ay), int(max(0, cx - 2.0 * ax)):int(cx + 2.0 * ax)]
        z = cv2.resize(z, (200, 200))
        if j == 0: cv2.putText(z, f"{i} {(k0 + 20) / 30:.0f}s", (3, 16), 0, 0.5, (0, 255, 255), 2)
        tiles.append(z)
    full = cv2.resize(fr[3], (150, 200))
    rows.append(np.hstack(tiles + [full]))
cv2.imwrite(outp, np.vstack(rows))

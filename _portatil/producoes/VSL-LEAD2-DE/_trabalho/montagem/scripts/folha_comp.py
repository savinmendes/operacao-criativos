import sys, cv2, numpy as np, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
out = sys.argv[1]; ids = sys.argv[2:]
rows = []
for i in ids:
    fr = ler(M/"comp"/f"{i}.mp4")
    info = json.load(open(M/"comp"/f"{i}.json"))
    cx, cy, ax, ay = info["elipse_media"]
    tiles = []
    for k in np.linspace(0, len(fr)-1, 4).astype(int):
        f = fr[k].copy()
        z = f[int(max(0,cy-2.2*ay)):int(cy+2.2*ay), int(max(0,cx-2.2*ax)):int(cx+2.2*ax)]
        z = cv2.resize(z, (240, int(240*z.shape[0]/max(1,z.shape[1]))))[:320]
        z = np.vstack([z, np.zeros((320-z.shape[0], 240, 3), np.uint8)])
        s = cv2.resize(f, (240, 320))
        cv2.putText(s, f"{i} k{k}", (5, 20), 0, 0.6, (0,255,255), 2)
        tiles += [s, z]
    rows.append(np.hstack(tiles))
cv2.imwrite(out, np.vstack(rows))

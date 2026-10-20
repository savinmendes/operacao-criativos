import sys, cv2, numpy as np, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
c = json.load(open(T/"base"/"cenas.json", encoding="utf-8"))["cenas"]
segs = [(x["ini"], x["fim"], x["tipo"]) for x in c if x["tipo"] in ("abertura_broll","igreja_geral","pulpito_vazio","estatua")]
tiles = []
for a, b, tp in segs:
    for t in (a + 0.3, (a + b) / 2, b - 0.3):
        f = ler(BASE, t, 1)[0]
        f = cv2.resize(f, (180, 240)); cv2.putText(f, f"{t:.1f}", (5, 20), 0, 0.6, (0,255,255), 2)
        tiles.append(f)
    tiles.append(np.zeros((240, 20, 3), np.uint8))
rows = []; row = []
per = 4*3
cols = 12
img = []
cur = []
for i in range(0, len(segs)):
    cur.append(np.hstack(tiles[i*4:(i+1)*4]))
    if len(cur) == 4: img.append(np.hstack(cur)); cur = []
if cur:
    w = img[0].shape[1] if img else sum(x.shape[1] for x in cur)
    r = np.hstack(cur); r = np.hstack([r, np.zeros((240, w - r.shape[1], 3), np.uint8)]) if img else r
    img.append(r)
cv2.imwrite(str(M/"chk"/"folha_broll.jpg"), np.vstack(img))
print(len(segs))

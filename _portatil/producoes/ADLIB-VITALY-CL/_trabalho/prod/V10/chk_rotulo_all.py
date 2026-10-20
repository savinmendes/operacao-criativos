import sys, json
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, "../comum"); import texto as T
import patch_rotulo as PR
fr = T.ler_quadros("orig.mp4", t=7.8)
ks = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(0, 232))
tiles = []
for k in ks:
    o = PR.RAS.get(k)
    g = PR.aplicar(fr[k], k)
    c = np.float32([[230, 680]] if (not o or o["a"] in (0, None)) else [[189, 715]])
    if o and o["M"] is not None:
        c = cv2.transform(c[None], np.float32(o["M"]))[0]
    cx, cy = int(c[0][0]), int(c[0][1])
    x0, y0 = min(max(0, cx - 110), 720 - 220), min(max(0, cy - 110), 1280 - 220)
    im = Image.fromarray(g[y0:y0 + 220, x0:x0 + 220]).resize((220, 220))
    ImageDraw.Draw(im).text((3, 3), str(k), fill="red")
    tiles.append(im)
cols = 10
sh = Image.new("RGB", (220 * cols, 220 * ((len(tiles) + cols - 1) // cols)))
for i, t in enumerate(tiles):
    sh.paste(t, ((i % cols) * 220, (i // cols) * 220))
sh.save(sys.argv[1])

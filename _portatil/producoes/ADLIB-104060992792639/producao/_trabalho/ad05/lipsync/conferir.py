"""Compara pt_<id>.mp4 (original) com ls_<id>.mp4 (lipsync): mapa médio de diferença; pico ~2/255 = lipsync não aconteceu."""
import sys, cv2, numpy as np
from pathlib import Path
L = Path(__file__).parent
for i in sys.argv[1:]:
    a, b = cv2.VideoCapture(str(L/f"pt_{i}.mp4")), cv2.VideoCapture(str(L/f"ls_{i}.mp4"))
    acc = None; n = 0; na=int(a.get(7)); nb=int(b.get(7))
    while True:
        ok1, f1 = a.read(); ok2, f2 = b.read()
        if not (ok1 and ok2): break
        if f2.shape != f1.shape: f2 = cv2.resize(f2, (f1.shape[1], f1.shape[0]))
        d = np.abs(f1.astype(np.int16)-f2.astype(np.int16)).mean(2)
        acc = d if acc is None else acc + d; n += 1
    m = cv2.blur(acc/n, (31,31)); y, x = np.unravel_index(m.argmax(), m.shape)
    print(f"{i}: quadros pt={na} ls={nb} | dif mediana={np.median(m):.2f} pico={m.max():.2f} em (x={x},y={y})")
    v = (np.clip(acc/n*8,0,255)).astype(np.uint8); cv2.imwrite(str(L/f"dif_{i}.jpg"), cv2.resize(v,(180,320)))

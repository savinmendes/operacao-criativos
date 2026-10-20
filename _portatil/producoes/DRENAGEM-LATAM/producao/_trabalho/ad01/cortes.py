import cv2, sys, numpy as np
v, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
c = cv2.VideoCapture(v); fps = c.get(5); c.set(1, int(a*fps)); i = int(a*fps); prev=None
while i < b*fps:
    ok, f = c.read()
    if not ok: break
    g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (90,160)).astype(float)
    if prev is not None:
        d = np.abs(g-prev).mean()
        if d > 18: print(f"{i/fps:.3f} (quadro {i}) diff {d:.0f}")
    prev = g; i += 1

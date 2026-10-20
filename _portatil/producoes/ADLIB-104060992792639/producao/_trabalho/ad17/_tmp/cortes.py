import cv2, numpy as np, sys
src = sys.argv[1]; tmax = float(sys.argv[2])
cap = cv2.VideoCapture(src); fps = cap.get(5); prev = None; i = 0; out = []
while True:
    ok, f = cap.read()
    if not ok or i / fps > tmax: break
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None:
        d = np.abs(g - prev).mean()
        if d > 12: out.append((i, round(i / fps, 3), round(d, 1)))
    prev = g; i += 1
print("fps", fps)
for o in out: print(o)

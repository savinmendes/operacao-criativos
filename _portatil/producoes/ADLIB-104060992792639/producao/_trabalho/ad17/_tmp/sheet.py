import cv2, sys, numpy as np
src, t0, t1, step, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 8
cap = cv2.VideoCapture(src); fps = cap.get(5)
ims = []
t = t0
while t <= t1:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*fps))); ok, f = cap.read()
    if not ok: break
    f = cv2.resize(f, (180, 320)); cv2.putText(f, f"{t:.2f}", (4, 18), 0, 0.55, (0,255,255), 2); ims.append(f); t += step
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i+cols]) for i in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80])

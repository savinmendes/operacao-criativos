import cv2, numpy as np, sys
cap = cv2.VideoCapture(sys.argv[1]); out = sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]
rows = []
for t in ts:
    f0 = round(t*30) - 3; tiles = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
    for k in range(6):
        ok, im = cap.read(); c = cv2.resize(im[150:1150, 140:940], (320, 400))
        cv2.putText(c, f"{(f0+k)/30:.3f}", (4, 20), 0, 0.6, (0,255,255), 2); tiles.append(c)
    rows.append(np.hstack(tiles))
cv2.imwrite(out, np.vstack(rows))

import cv2, glob, sys, numpy as np, os
src, out, step, t0, cols, w = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
fs = sorted(glob.glob(os.path.join(src, "*.jpg")))
ims = []
for i, f in enumerate(fs):
    im = cv2.imread(f); im = cv2.resize(im, (w, int(im.shape[0] * w / im.shape[1])))
    cv2.putText(im, f"{t0 + i*step:.1f}", (4, 24), 0, 0.7, (0, 255, 255), 2); ims.append(im)
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i+cols]) for i in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])

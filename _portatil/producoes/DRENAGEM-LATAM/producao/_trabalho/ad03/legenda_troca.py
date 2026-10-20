import cv2, numpy as np, sys
cap = cv2.VideoCapture('full_up720.mp4')
def mask(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * 30)))
    ok, f = cap.read(); r = f[880:1010, :]
    h = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    return ((h[..., 2] > 235) & (h[..., 1] < 25)).astype(np.uint8)
def trocas(t0, t1):
    out = []; prev = mask(t0)
    for k in range(1, int((t1 - t0) * 30) + 1):
        t = t0 + k / 30; m = mask(t)
        d = np.mean(m != prev)
        if d > 0.04: out.append((round(t, 3), round(float(d), 3)))
        prev = m
    return out
for s in [84.695, 98.89, 113.25, 159.27, 199.065, 252.33, 269.39, 322.31, 370.05, 392.53, 531.22, 611.59, 640.51, 439.53, 578.59]:
    s = round(s * 30) / 30
    print('ini', s, trocas(s, s + 1.6))
print('fim 138.40', trocas(136.9, 138.45))

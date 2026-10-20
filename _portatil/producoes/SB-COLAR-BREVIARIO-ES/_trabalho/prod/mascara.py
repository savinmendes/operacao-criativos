import cv2, numpy as np
Y0, Y1 = 1060, 1360
def mascara(f):
    roi = f[Y0:Y1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[...,0], hsv[...,1], hsv[...,2]
    branco = (s < 45) & (v > 200)
    verm = ((h < 8) | (h > 170)) & (s > 140) & (v > 140)
    escuro = (v < 50).astype(np.uint8)
    perto = cv2.dilate(escuro, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    core = ((branco | verm).astype(np.uint8) & perto)
    n, lab, st, cen = cv2.connectedComponentsWithStats(core)
    keep = np.zeros(n, bool)
    for k in range(1, n):
        x, y, w, hh, a = st[k]
        if a >= 30 and hh <= 110 and w <= 200: keep[k] = True
    core = keep[lab].astype(np.uint8)
    core[:, :100] = 0; core[:, 970:] = 0
    if core.sum() < 200: return np.zeros(f.shape[:2], np.uint8)
    # linhas de texto: concentra em faixa horizontal
    rows = core.sum(1); ys = np.where(rows > 3)[0]
    d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    dn = np.zeros_like(d); dn[5:] = d[:-5]
    m = cv2.dilate(d | dn, np.ones((7, 7), np.uint8))
    full = np.zeros(f.shape[:2], np.uint8); full[Y0:Y1] = m
    return full
if __name__ == "__main__":
    import sys
    ims = []
    for t in sys.argv[1:]:
        cap = cv2.VideoCapture("../../original_wsen5drS7Nk.mp4"); cap.set(cv2.CAP_PROP_POS_FRAMES, int(float(t)*30)); ok, f = cap.read()
        m = mascara(f); o = f.copy(); o[m > 0] = (0.5*o[m > 0] + [0,127,0]).astype(np.uint8)
        ims.append(cv2.resize(o[900:1500], (540, 300)))
    cv2.imwrite("q/mask_prev.jpg", np.vstack(ims))

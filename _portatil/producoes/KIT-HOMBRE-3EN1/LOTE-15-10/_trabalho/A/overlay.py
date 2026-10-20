import cv2, numpy as np
cap = cv2.VideoCapture('venc_hd.mp4'); fps = cap.get(5); fr = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i > 8.2*fps and i % 9 == 0: fr.append(f)
    i += 1
S = np.stack(fr).astype(np.float32); print(S.shape)
med = np.median(S, 0); sd = S.std(0).max(-1)
a = (sd < 9).astype(np.uint8)
# só nas regiões do selo e do rodapé
reg = np.zeros_like(a); reg[20:125, 0:500] = 1; reg[895:1200, 140:580] = 1
a &= reg
a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((3,3),np.uint8)); a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(a)
keep = np.zeros_like(a)
for k in range(1, n):
    if st[k, cv2.CC_STAT_AREA] > 400: keep[lab == k] = 1
# preencher buracos internos
cnts, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
fill = np.zeros_like(keep); cv2.drawContours(fill, cnts, -1, 1, -1)
al = cv2.erode(fill, np.ones((3,3),np.uint8)).astype(np.float32)
al = cv2.GaussianBlur(al, (0,0), 0.8)
rgba = np.dstack([med, al*255]).astype(np.uint8)
cv2.imwrite('overlay_selo_rodape.png', rgba)
sel = rgba.copy(); sel[400:] = 0; cv2.imwrite('overlay_selo.png', sel)
rod = rgba.copy(); rod[:400] = 0; cv2.imwrite('overlay_rodape.png', rod)
# preview sobre cinza
bg = np.full_like(med, 128); prev = med*al[...,None] + bg*(1-al[...,None]); cv2.imwrite('q/overlay_prev.jpg', prev.astype(np.uint8))

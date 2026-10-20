# caixas da legenda queimada por quadro -> _tmp/boxmasks.npy (N,70,720) uint8, faixa y 960-1030
import cv2, numpy as np
Y0, Y1 = 960, 1030
cap = cv2.VideoCapture('../../../UNICOS_HD/13.mp4'); xr = []
while True:
    ok, f = cap.read()
    if not ok: break
    roi = f[978:1020]
    b, g, r = cv2.split(roi.astype(np.int16)); gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    txt = ((np.minimum(r, g) > 160) & (gray > 140)).astype(np.uint8) & cv2.dilate((gray < 70).astype(np.uint8), np.ones((5, 5), np.uint8))
    ys, xs = np.nonzero(txt)
    xr.append((np.percentile(xs, 0.5), np.percentile(xs, 99.5)) if len(xs) > 40 else None)
N = len(xr); B = np.zeros((N, Y1 - Y0, 720), np.uint8)
for i in range(N):
    for j in range(max(0, i - 2), min(N, i + 3)):      # uniao temporal +-2 quadros (entrada/saida das palavras)
        if xr[j]:
            x0, x1 = xr[j]
            B[i, 972 - Y0:1024 - Y0, max(0, int(x0) - 14):int(x1) + 15] = 1
np.save('_tmp/boxmasks.npy', B)
w = [(x[1]-x[0]) for x in xr if x]; print('N', N, 'com', len(w), 'largura med', np.median(w), 'max', max(w))

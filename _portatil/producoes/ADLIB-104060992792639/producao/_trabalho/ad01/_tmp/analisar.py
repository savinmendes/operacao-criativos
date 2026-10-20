"""Passo 1: máscaras da legenda (amarela, contorno preto) por quadro, placas medianas por tomada e escore de movimento."""
import cv2, numpy as np, warnings
warnings.filterwarnings("ignore")
SRC = '../../../UNICOS_HD/01.mp4'
Y0, Y1 = 820, 990
NF = 3473
SHOTS = [(0, 477), (477, 584), (584, 629), (629, 979), (979, 1470), (1470, 3473)]

def mascara(roi):
    b, g, r = cv2.split(roi.astype(np.int16)); gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    yel = ((r > 150) & (g > 150) & (b < 150) & (np.minimum(r, g) - b > 40)).astype(np.uint8)
    yel &= cv2.dilate((gray < 70).astype(np.uint8), np.ones((7, 7), np.uint8))
    yel = cv2.morphologyEx(yel, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    m = cv2.dilate(yel, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
    # caixas por componente (linha) para pegar contorno/sombra inteiros
    out = np.zeros_like(m)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a < 150: continue
        out[max(0, y - 3):y + h + 3, max(0, x - 4):x + w + 4] = 1
    return out

cap = cv2.VideoCapture(SRC)
R = np.zeros((NF, Y1 - Y0, 720, 3), np.uint8); BM = np.zeros((NF, Y1 - Y0, 720), np.uint8)
for i in range(NF):
    ok, f = cap.read()
    R[i] = f[Y0:Y1]; BM[i] = mascara(R[i])
np.save('_tmp/boxmasks.npy', BM); np.save('_tmp/rois.npy', R)
placas = []
for a, b in SHOTS:
    idx = list(range(a, b, max(1, (b - a) // 350)))
    st = R[idx].astype(np.float32); mk = BM[idx].astype(bool)
    st[mk] = np.nan
    p = np.nanmedian(st, axis=0); bur = np.isnan(p).any(2)
    print('tomada', a, b, 'buracos', int(bur.sum()), flush=True)
    p = np.nan_to_num(p).astype(np.uint8)
    np.save(f'_tmp/buraco_{a}.npy', bur)
    placas.append(p)
np.save('_tmp/placas.npy', np.stack(placas))
cv2.imwrite('_tmp/placas.png', np.vstack(placas))
sc = np.zeros(NF)
for s, (a, b) in enumerate(SHOTS):
    P = placas[s].astype(np.float32)
    for i in range(a, b):
        m = cv2.dilate(BM[i], np.ones((9, 9), np.uint8))
        d = np.abs(R[i].astype(np.float32) - P).mean(2); free = (m == 0)
        sc[i] = max((d[:, x:x + 40] * free[:, x:x + 40]).sum() / max(1, free[:, x:x + 40].sum()) for x in range(0, 720, 40))
np.save('_tmp/mov.npy', sc)
for thr in [8, 10, 12, 15, 20]: print(thr, int((sc > thr).sum()))
for s, (a, b) in enumerate(SHOTS): print(a, b, 'mediana mov', round(float(np.median(sc[a:b])), 1), 'max', round(float(sc[a:b].max()), 1))

"""Folha de 1 em 1 quadro em volta de cada corte do vídeo final: python folha_cortes.py final.mp4 saida.jpg t1,t2,..."""
import sys, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS); rows = []
for t in [float(x) for x in sys.argv[3].split(",")]:
    k0 = int(round(t * fps)); ims = []
    for k in range(k0 - 3, k0 + 4):
        cap.set(cv2.CAP_PROP_POS_FRAMES, k); ok, f = cap.read()
        if not ok: f = np.zeros((1280, 720, 3), np.uint8)
        f = cv2.resize(f, (108, 192)); cv2.putText(f, f"{k/fps:.2f}", (2, 12), 0, 0.38, (0, 255, 255), 1); ims.append(f)
    rows.append(np.hstack(ims))
h = len(rows) // 2 + len(rows) % 2
L, R = rows[:h], rows[h:]
while len(R) < len(L): R.append(np.zeros_like(L[0]))
cv2.imwrite(sys.argv[2], np.hstack([np.vstack(L), np.full((192 * h, 8, 3), 255, np.uint8), np.vstack(R)])); print(sys.argv[2])

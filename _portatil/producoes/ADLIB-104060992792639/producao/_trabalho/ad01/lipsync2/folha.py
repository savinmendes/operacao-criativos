import sys, cv2, numpy as np
from pathlib import Path
import medir as Me
clip, q0, k0, k1, saida = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
es = Me.env('es', Path(__file__).resolve().parent.parent / 'narracao_es.wav')
cap = cv2.VideoCapture(clip); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
tiles = []
for k in range(k0, k1, 2):
    m = cv2.resize(fr[k][330:580, 320:530], None, fx=1.2, fy=1.2)
    col = (0, 255, 0) if es[q0 + k] > np.nanmax(es) - 30 else (0, 0, 255)
    cv2.rectangle(m, (0, 0), (m.shape[1], 10), col, -1); cv2.putText(m, '%.2f' % ((q0 + k) / 30), (4, m.shape[0] - 6), 0, 0.55, (255, 255, 255), 2)
    tiles.append(m)
while len(tiles) % 10: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(saida, cv2.resize(np.vstack([np.hstack(tiles[i:i + 10]) for i in range(0, len(tiles), 10)]), None, fx=0.55, fy=0.55))

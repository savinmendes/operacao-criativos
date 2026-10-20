import sys, numpy as np, cv2
vid, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
e = np.load('diag_env.npy'); thr = e.max() - 30
cap = cv2.VideoCapture(vid); fps = 25
tiles = []
for i in range(int(t0 * fps), int(t1 * fps), 2):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i); ok, f = cap.read()
    c = cv2.resize(f[380:500, 300:470], (170, 120))
    fala = e[i] > thr
    cv2.putText(c, f"{i/fps:.2f} {'F' if fala else 'P'}", (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0) if fala else (0, 0, 255), 1)
    tiles.append(c)
while len(tiles) % 8: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[k:k + 8]) for k in range(0, len(tiles), 8)]))

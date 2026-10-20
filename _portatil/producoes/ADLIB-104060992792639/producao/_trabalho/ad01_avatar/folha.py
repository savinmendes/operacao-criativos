import sys, numpy as np, cv2
vid = sys.argv[1]; out = sys.argv[2]
ab = np.load('diag_ab.npy'); env = np.load('diag_env.npy')
fps = 25.0
thr = np.nanmax(env) - 30
fala = env > thr
# escolher quadros: 12 de pausa (miolo de corridas >=8) e 12 de fala
idx_p, idx_f = [], []
run = 0
for i, v in enumerate(list(fala) + [True]):
    if not v: run += 1
    else:
        if run >= 8: idx_p.append(i - run // 2 - 1)
        run = 0
idx_f = [i for i in range(0, len(fala), 97) if fala[i]]
rng = np.random.default_rng(0)
idx_p = sorted(rng.choice(idx_p, min(12, len(idx_p)), replace=False))
idx_f = sorted(rng.choice(idx_f, min(12, len(idx_f)), replace=False))
cap = cv2.VideoCapture(vid)
tiles = []
for lab, L in (("PAUSA", idx_p), ("FALA", idx_f)):
    row = []
    for i in L:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, f = cap.read()
        c = cv2.resize(f[380:500, 300:470], (255, 180))
        cv2.putText(c, f"{lab} {i/fps:.2f}s", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255) if lab == "PAUSA" else (0, 255, 0), 1)
        cv2.putText(c, f"ab {ab[i]:.3f}", (4, 172), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        row.append(c)
    tiles.append(np.vstack([np.hstack(row[k:k + 6]) for k in range(0, 12, 6)]))
cv2.imwrite(out, np.vstack(tiles))
print(len(idx_p), len(idx_f))

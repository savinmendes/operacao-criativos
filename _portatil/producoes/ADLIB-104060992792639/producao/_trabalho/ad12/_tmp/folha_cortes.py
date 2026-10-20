import cv2, numpy as np, sys
v, out = sys.argv[1], sys.argv[2]; cortes = [float(x) for x in sys.argv[3].split(",")]
cap = cv2.VideoCapture(v); fps = cap.get(5); rows = []
for t in cortes:
    c = int(round(t * fps)); row = []
    for k in range(c - 4, c + 5):
        cap.set(1, k); ok, f = cap.read()
        if not ok: f = np.zeros((1280, 720, 3), np.uint8)
        z = cv2.resize(f[200:900, 160:620], (138, 210)); cv2.putText(z, f"{k/fps:.2f}", (3, 14), 0, 0.42, (0, 255, 0), 1); row.append(z)
    rows.append(np.hstack(row))
cv2.imwrite(out, np.vstack(rows))

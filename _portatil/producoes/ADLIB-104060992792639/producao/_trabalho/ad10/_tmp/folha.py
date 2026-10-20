"""Folha de contato: python folha.py video.mp4 saida.jpg ini fim passo [larg] [cols] [y0:y1 recorte]"""
import sys, cv2, numpy as np
v, out, a, b, p = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
W = int(sys.argv[6]) if len(sys.argv) > 6 else 180; C = int(sys.argv[7]) if len(sys.argv) > 7 else 8
rec = [int(x) for x in sys.argv[8].split(":")] if len(sys.argv) > 8 else None
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS); ims = []
t = a
while t <= b + 1e-6:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps))); ok, f = cap.read()
    if not ok: break
    if rec: f = f[rec[0]:rec[1]]
    h = int(f.shape[0] * W / f.shape[1]); f = cv2.resize(f, (W, h))
    cv2.putText(f, f"{t:.2f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3); cv2.putText(f, f"{t:.2f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    ims.append(f); t += p
while len(ims) % C: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i + C]) for i in range(0, len(ims), C)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out, len(ims))

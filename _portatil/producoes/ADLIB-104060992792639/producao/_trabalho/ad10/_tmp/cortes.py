"""Detecta cortes (diferença média de quadro pequeno) num vídeo. Uso: python cortes.py video.mp4 [max_s]"""
import sys, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS)
mx = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
prev = None; i = 0; d = []
while True:
    ok, f = cap.read()
    if not ok or i / fps > mx: break
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None: d.append((i, np.abs(g - prev).mean()))
    prev = g; i += 1
arr = np.array([x[1] for x in d]); med = np.median(arr)
print("fps", fps, "quadros", i, "mediana", round(med, 2))
for k, v in d:
    if v > max(12, 5 * med): print(f"corte q{k} t={k/fps:.3f} dif={v:.1f}")

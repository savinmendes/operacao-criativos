"""Confere cada lipsync: quadros, região da boca (pico da diferença) vs ruído fora do rosto."""
import sys, cv2, numpy as np
for n in sys.argv[1:]:
    ca, cb = cv2.VideoCapture(f"pt_{n}.mp4"), cv2.VideoCapture(f"ls_{n}.mp4")
    na, nb = int(ca.get(7)), int(cb.get(7)); acc = None; k = 0
    while True:
        oa, a = ca.read(); ob, b = cb.read()
        if not (oa and ob): break
        if b.shape != a.shape: b = cv2.resize(b, (a.shape[1], a.shape[0]))
        d = np.abs(a.astype(np.float32) - b).mean(2); acc = d if acc is None else acc + d; k += 1
    acc /= k; bl = cv2.blur(acc, (61, 41)); y, x = np.unravel_index(bl[100:800].argmax(), bl[100:800].shape); y += 100
    boca = acc[y-40:y+40, x-60:x+60].mean(); ruido = np.median(acc[850:1250])
    print(f"{n} quadros pt={na} ls={nb} boca@({x},{y}) dif={boca:.1f} ruido={ruido:.1f} {'OK' if boca > 3*ruido and boca > 5 else 'FALHOU?'}")

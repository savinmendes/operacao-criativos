# folha original x antes x depois (quadro inteiro reduzido + zoom no rosto) em alguns tempos -> _cor_rev/folha_cor.jpg
import sys, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
P = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639"
FIN = P + r"\producao\AD 07 - ORACION-CINTA-BLANCA-ES-LATAM.mp4"; ANT = P + r"\producao\_trabalho\ad07\_antes_cor\AD 07 - ORACION-CINTA-BLANCA-ES-LATAM.mp4"; ORI = P + r"\UNICOS_HD\07.mp4"
TS = [2.0, 12.0, 30.0, 47.0, 54.0, 66.0, 76.0, 86.0]
def q(p, i): return next(quadros(p, i, 1))
rows = []
for t in TS:
    o, a, d = q(ORI, round(t * 24)), q(ANT, round(t * 30)), q(FIN, round(t * 30))
    small = [cv2.resize(x, (180, 320)) for x in (o, a, d)]
    zoom = [cv2.resize(x[380:780, 270:570], (240, 320)) for x in (o, a, d)]
    r = np.hstack(small + zoom); cv2.putText(r, f"{t:.0f}s", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2); rows.append(r)
hdr = np.zeros((30, rows[0].shape[1], 3), np.uint8)
for k, s in enumerate(["original", "antes", "depois"]):
    cv2.putText(hdr, s, (5 + 180 * k, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1); cv2.putText(hdr, s + " (zoom)", (545 + 240 * k, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
cv2.imwrite(P + r"\producao\_trabalho\ad07\_cor_rev\folha_cor.jpg", np.vstack([hdr] + rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print("ok")

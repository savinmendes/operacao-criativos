import json, cv2, numpy as np
from pathlib import Path
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
esc = json.loads(Path("escolha_06.json").read_text()); t = esc["w15"][2]
cf = cv2.VideoCapture(str(P/"producao"/"AD 06 - ORACION-NUDO-ES-LATAM.mp4")); co = cv2.VideoCapture(str(P/"UNICOS_HD"/"06.mp4"))
r = []
for q, cx, cy, L in t[::3]:
    cf.set(1, q); ok, f = cf.read(); co.set(1, int(round(q*24/30))); ok, o = co.read()
    Y = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2YUV)[:, :, 0].astype(float)
    yf, yo = Y(f), Y(o)
    bx = lambda y, x0, y0, w, h: y[int(y0-h/2):int(y0+h/2), int(x0-w/2):int(x0+w/2)]
    a = [bx(yf, cx, cy-0.17*L, 0.30*L, 0.08*L).mean()-bx(yo, cx, cy-0.17*L, 0.30*L, 0.08*L).mean(),
         bx(yf, cx, cy+0.30*L, 0.30*L, 0.12*L).mean()-bx(yo, cx, cy+0.30*L, 0.30*L, 0.12*L).mean(),
         np.median(bx(yf, cx, cy+0.30*L, 0.30*L, 0.12*L)-bx(yo, cx, cy+0.30*L, 0.30*L, 0.12*L)),
         np.median(bx(yf, cx-0.25*L, cy+0.05*L, 0.12*L, 0.12*L)-bx(yo, cx-0.25*L, cy+0.05*L, 0.12*L, 0.12*L))]
    r.append(a)
r = np.array(r); print("w15: labio sup (media) | queixo (media) | queixo (mediana) | canto da boca/bochecha baixa (mediana)"); print(np.median(r, 0).round(1))

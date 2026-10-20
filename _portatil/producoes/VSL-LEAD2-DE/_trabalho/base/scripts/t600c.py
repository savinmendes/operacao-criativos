import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from limpar import preparar
f = cv2.imread("amostras_src/t600.png"); u, mk, _ = preparar(f, [[66,792,644,838],[216,836,412,875],[393,842,503,874]])
v = u.copy(); v[mk > 0] = (v[mk > 0] * 0.5 + np.array([255, 0, 255]) * 0.5).astype(np.uint8)
c = np.vstack([u[780:880, 50:350], v[780:880, 50:350]]); cv2.imwrite("teste_m600.png", cv2.resize(c, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST))

import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from limpar import preparar, inpaint
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
B = {"t1500":[[37,795,289,840],[287,792,669,834],[324,835,398,880]],"t20":[[65,692,658,749]],"t330":[[97,694,554,742],[535,705,605,731],[179,741,541,780]],
     "t2300":[[125,767,585,801],[88,806,631,849]],"t600":[[66,792,644,838],[216,836,412,875],[393,842,503,874]],"t2450":[[88,765,620,805],[311,813,410,848]]}
outs = []
for k, bx in B.items():
    f = cv2.imread(f"amostras_src/{k}.png"); u, mk, modos = preparar(f, bx); print(k, modos)
    o = inpaint(lama, u, mk); outs.append(np.vstack([f[640:960], o[640:960]]))
cv2.imwrite("teste_limpar.jpg", np.hstack(outs))
z = []
for k in ["t600", "t2300", "t1500"]:
    f = cv2.imread(f"amostras_src/{k}.png"); u, mk, _ = preparar(f, B[k]); o = inpaint(lama, u, mk)
    z.append(np.vstack([f[740:900, 0:720], o[740:900, 0:720], cv2.cvtColor(mk[740:900]*255, cv2.COLOR_GRAY2BGR)]))
cv2.imwrite("teste_zoom.png", np.vstack(z))

import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from caixa import bordas, razao
B = {"t1500":[[37,795,289,840],[287,792,669,834],[324,835,398,880]],
     "t2300":[[125,767,585,801],[88,806,631,849]],"t600":[[66,792,644,838],[216,836,412,875],[393,842,503,874]],"t2450":[[88,765,620,805],[311,813,410,848]]}
for k, bx in B.items():
    f = cv2.imread(f"amostras_src/{k}.png"); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    for b in bx:
        c, s = bordas(g, b); print(k, b, "->", c, [round(float(x),1) for x in s], [round(float(x),3) for x in razao(g, c)])

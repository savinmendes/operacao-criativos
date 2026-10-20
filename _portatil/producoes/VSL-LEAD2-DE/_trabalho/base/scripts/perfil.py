import cv2, numpy as np, sys, time; sys.path.insert(0, "scripts")
import limpar
from limpar import preparar
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
f = cv2.imread("amostras_src/t2300.png"); bx = [[125,767,585,801],[88,806,631,849]]
for _ in range(2): preparar(f, bx)
t = time.time(); [preparar(f, bx) for _ in range(5)]; print("preparar", (time.time()-t)/5)
u, mk, _ = preparar(f, bx)
ys = np.where(mk.any(1))[0]; a0 = max(0, ys.min() - 90); a1 = min(960, ys.max() + 60); crop = u[a0:a1]; m = mk[a0:a1]
for _ in range(2): r = lama(Image.fromarray(crop), Image.fromarray(m * 255))
t = time.time(); [lama(Image.fromarray(crop), Image.fromarray(m * 255)) for _ in range(5)]; print("lama", (time.time()-t)/5, crop.shape)
r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
t = time.time(); [cv2.inpaint(crop, m, 5, cv2.INPAINT_TELEA) for _ in range(3)]; print("telea", (time.time()-t)/3)

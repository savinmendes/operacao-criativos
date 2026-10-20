import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from limpar import preparar
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
f = cv2.imread("amostras_src/t600.png"); u, mk, _ = preparar(f, [[66,792,644,838],[216,836,412,875],[393,842,503,874]])
outs = []
for ctx in [90, 250, 500]:
    ys = np.where(mk.any(1))[0]; a0 = max(0, ys.min() - ctx); a1 = 960
    r = lama(Image.fromarray(cv2.cvtColor(u[a0:a1], cv2.COLOR_BGR2RGB)), Image.fromarray(mk[a0:a1] * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:a1-a0, :720]; o = u.copy(); o[a0:a1] = r
    outs.append(o[740:900])
outs.append(u[740:900])
cv2.imwrite("teste_t600.png", np.vstack(outs))

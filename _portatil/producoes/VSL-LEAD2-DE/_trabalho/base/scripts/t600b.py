import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from limpar import preparar
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
f = cv2.imread("amostras_src/t600.png"); u, mk, _ = preparar(f, [[66,792,644,838],[216,836,412,875],[393,842,503,874]])
a0=600
def L(img, m):
    r = lama(Image.fromarray(cv2.cvtColor(img[a0:], cv2.COLOR_BGR2RGB)), Image.fromarray(m[a0:] * 255))
    return cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:960-a0, :720]
o1 = L(u, mk)
u2 = cv2.resize(u, (360, 480), interpolation=cv2.INTER_AREA); m2 = (cv2.resize(mk, (360, 480)) > 0).astype(np.uint8)
r2 = lama(Image.fromarray(cv2.cvtColor(u2, cv2.COLOR_BGR2RGB)), Image.fromarray(m2 * 255)); r2 = cv2.cvtColor(np.array(r2), cv2.COLOR_RGB2BGR)[:480,:360]
r2 = cv2.resize(r2, (720, 960), interpolation=cv2.INTER_CUBIC)[a0:]; o2 = np.where(mk[a0:, :, None] > 0, r2, u[a0:])
o3 = cv2.inpaint(u, mk, 5, cv2.INPAINT_TELEA)[a0:]
print(u[a0:].dtype, u.flags['C_CONTIGUOUS'])
cv2.imwrite("teste_t600.png", np.vstack([x[140:300] for x in [o1, o2, o3]]))

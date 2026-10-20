import cv2, numpy as np, sys; sys.path.insert(0, "scripts")
from limpar import preparar
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
f = cv2.imread("amostras_src/t600.png"); u, mk, _ = preparar(f, [[66,792,644,838],[216,836,412,875],[393,842,503,874]])
a0 = 600; res = []
for pre in ["nada", "zero", "telea"]:
    x = u.copy()
    if pre == "zero": x[mk > 0] = 0
    if pre == "telea": x = cv2.inpaint(u, mk, 5, cv2.INPAINT_TELEA)
    r = lama(Image.fromarray(cv2.cvtColor(x[a0:], cv2.COLOR_BGR2RGB)), Image.fromarray(mk[a0:] * 255))
    res.append(cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[140:300, :720])
cv2.imwrite("teste_t600.png", np.vstack(res))

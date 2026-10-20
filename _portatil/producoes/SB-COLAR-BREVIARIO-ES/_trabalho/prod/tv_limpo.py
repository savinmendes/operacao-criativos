import cv2, numpy as np, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
from comum3 import quadros
f = next(quadros("../../original_wsen5drS7Nk.mp4", 670, 1, 1080, 1920))
cv2.imwrite("q/tv670_bt601.png", f)
m = np.zeros(f.shape[:2], np.uint8)
m[25:100, 30:1050] = 1          # faixa preta topo
m[778:842, 100:910] = 1         # tarja branca
m[845:1050, 80:990] = 1         # texto amarelo na caixa vermelha
m[1225:1355, 60:830] = 1        # legenda borrada antiga
lama = SimpleLama()
r = lama(Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:1920, :1080]
cv2.imwrite("q/tv670_limpo.png", r)

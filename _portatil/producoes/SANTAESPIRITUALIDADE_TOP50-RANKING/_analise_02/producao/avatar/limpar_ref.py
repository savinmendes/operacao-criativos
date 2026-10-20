import numpy as np, cv2, sys
from PIL import Image
from simple_lama_inpainting import SimpleLama
f = np.asarray(Image.open("avatar/o_40.5.png").convert("RGB"))
m = np.zeros(f.shape[:2], np.uint8)
m[690:770, 200:520] = 1      # legenda
m[20:150, 30:700] = 1        # moldura da live
m[1140:1260, 10:715] = 1     # barra de comentário
r = np.array(SimpleLama()(Image.fromarray(f), Image.fromarray(m * 255)))[:1280, :720]
Image.fromarray(r).save("avatar/cena_padre_limpa.png"); print("ok")

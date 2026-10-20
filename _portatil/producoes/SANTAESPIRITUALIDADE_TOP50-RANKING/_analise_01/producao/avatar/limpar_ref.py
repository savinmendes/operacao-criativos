import numpy as np, cv2
from PIL import Image
from simple_lama_inpainting import SimpleLama
f=np.asarray(Image.open("ref/o_30.png").convert("RGB"))
m=np.zeros(f.shape[:2],np.uint8)
m[640:730,160:560]=1      # legenda
m[40:150,30:670]=1        # moldura da live
m[1170:1270,15:700]=1     # barra de comentário
r=np.array(SimpleLama()(Image.fromarray(f),Image.fromarray(m*255)))[:1280,:720]
Image.fromarray(r).save("avatar/cena_frade_limpa.png"); print("ok")

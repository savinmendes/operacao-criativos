import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
l=SimpleLama(); im=cv2.imread('card_med.png'); m=cv2.imread('card_mask.png',0)
r=l(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)),Image.fromarray(m))
r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:1280,:720]
a=(cv2.GaussianBlur((m>0).astype(np.float32),(7,7),0)[...,None]); a=np.maximum(a,(m>0)[...,None])
cv2.imwrite('card_limpo.png',(r*a+im*(1-a)).astype(np.uint8))

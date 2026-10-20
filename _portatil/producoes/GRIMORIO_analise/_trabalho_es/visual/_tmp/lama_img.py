import sys, cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
l=SimpleLama(); im=cv2.imread(sys.argv[1]); m=cv2.imread(sys.argv[2],0)
r=l(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)),Image.fromarray(m))
r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:im.shape[0],:im.shape[1]]
cv2.imwrite(sys.argv[3],r)

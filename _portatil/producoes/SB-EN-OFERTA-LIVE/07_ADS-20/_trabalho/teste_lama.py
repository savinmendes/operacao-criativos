import cv2,numpy as np,sys
from PIL import Image
from simple_lama_inpainting import SimpleLama
from mascara import mascara
lama=SimpleLama(); out=[]
for p in sys.argv[1:]:
    f=cv2.imread(p); m=mascara(f)
    a0,a1=700,1200
    r=lama(Image.fromarray(cv2.cvtColor(f[a0:a1],cv2.COLOR_BGR2RGB)),Image.fromarray(m[a0:a1]*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:a1-a0,:720]
    vis=f[a0:a1].copy(); vis[m[a0:a1]>0]=(0,0,255)
    out.append(cv2.vconcat([cv2.resize(vis,(360,250)),cv2.resize(r,(360,250))]))
cv2.imwrite('teste_lama.jpg',cv2.hconcat(out))

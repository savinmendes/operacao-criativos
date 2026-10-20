import json,sys,cv2,numpy as np,warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
k=int(sys.argv[1]); B={int(a):v for a,v in json.load(open("../ocr_boxes.json")).items()}
f=cv2.imread(f"cand/k{k}.png"); H,W=f.shape[:2]; m=np.zeros((H,W),np.uint8)
for j in range(k-2,k+3):
    for x0,y0,x1,y1 in B.get(j,[]):
        print(j,x0,y0,x1,y1); m[max(0,y0-22):y1+22,max(0,x0-24):min(W,x1+24)]=1
r=SimpleLama()(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),Image.fromarray(m*255))
r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:H,:W]
cv2.imwrite(f"cand/k{k}_limpo.png",r); cv2.imwrite(f"cand/k{k}_zoom.jpg",np.hstack([f[1200:1600,100:980],r[1200:1600,100:980]]))

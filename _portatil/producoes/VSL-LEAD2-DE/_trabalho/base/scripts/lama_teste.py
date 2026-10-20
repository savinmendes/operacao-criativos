import cv2, numpy as np, torch, sys
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama = SimpleLama()
B = {"t1500":[[37,795,289,840],[287,792,669,834],[324,835,398,880]],"t20":[[65,692,658,749]],"t200":[[4,693,716,749]],
     "t2300":[[125,767,585,801],[88,806,631,849]],"t600":[[66,792,644,838],[216,836,412,875],[393,842,503,874]]}
PAD=int(sys.argv[1]) if len(sys.argv)>1 else 8
outs=[]
for k,bx in B.items():
    f=cv2.imread(f"amostras_src/{k}.png"); m=np.zeros(f.shape[:2],np.uint8)
    for x0,y0,x1,y1 in bx: m[max(0,y0-PAD):y1+PAD, max(0,x0-PAD):x1+PAD]=1
    a0=560; crop=f[a0:]; r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(m[a0:]*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    g=f.copy(); g[a0:]=np.where(m[a0:,:,None]>0,r,crop)
    outs.append(np.vstack([f[600:960],g[600:960]]))
cv2.imwrite("teste_lama.jpg",np.hstack(outs))

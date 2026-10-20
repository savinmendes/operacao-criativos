import cv2,numpy as np,warnings;warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
lama=SimpleLama();Y0,Y1=960,1090;C0,C1=820,1230
def tight(roi,d):
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    core=((h>=15)&(h<=42)&(s>=80)&(v>=140)).astype(np.uint8)&cv2.dilate((v<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    out=(v<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    return cv2.dilate(cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))|out,np.ones((d,d),np.uint8))
MK=np.load('_fix/lama_mask.npy',mmap_mode='r')
c=cv2.VideoCapture('../../../UNICOS_HD/05.mp4');rows=[]
for i in [1500,1582,1650,1730,1900,2100]:
    c.set(1,i);_,f=c.read();crop=f[C0:C1].copy()
    res=[f[930:1120]]
    for kind in ['box','t5','t9']:
        mk=np.zeros(crop.shape[:2],np.uint8)
        if kind=='box': mk[940-C0:1110-C0]=np.array(MK[i])
        else: mk[Y0-C0:Y1-C0]=tight(f[Y0:Y1],5 if kind=='t5' else 9)
        r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
        r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
        res.append(r[930-C0:1120-C0])
    rows.append(cv2.resize(np.hstack(res),(1440,95)))
cv2.imwrite('_fix/teste_mask.jpg',np.vstack(rows))

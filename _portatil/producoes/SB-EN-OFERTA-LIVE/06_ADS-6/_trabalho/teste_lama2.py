import warnings; warnings.filterwarnings("ignore")
import cv2,numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
from mascara2 import mascara
lama=SimpleLama()
def limpar(f,m,esc=0.5):
    H,W=m.shape
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-160); a1=min(H,ys.max()+160)
    crop=f[a0:a1]; mk=m[a0:a1]
    cs=cv2.resize(crop,None,fx=esc,fy=esc,interpolation=cv2.INTER_AREA)
    ms=(cv2.resize(mk.astype(np.uint8)*255,(cs.shape[1],cs.shape[0]),interpolation=cv2.INTER_NEAREST)>0).astype(np.uint8)
    ms=cv2.dilate(ms,np.ones((3,3),np.uint8))
    r=lama(Image.fromarray(cv2.cvtColor(cs,cv2.COLOR_BGR2RGB)),Image.fromarray(ms*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:cs.shape[0],:cs.shape[1]]
    r=cv2.resize(r,(crop.shape[1],crop.shape[0]),interpolation=cv2.INTER_CUBIC).astype(np.float32)
    al=cv2.GaussianBlur(cv2.dilate(mk,np.ones((9,9),np.uint8)).astype(np.float32),(21,21),0)[...,None]
    out=f.copy(); out[a0:a1]=np.clip(r*al+crop*(1-al),0,255).astype(np.uint8); return out
if __name__=="__main__":
    s=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"); rows=[]
    for t in [7.6,107.2,119.5,130.4,32.5]:
        fi=int(t/1.0087*30); s.set(1,fi); _,f=s.read(); m=mascara(f)
        rows.append(np.hstack([cv2.resize(limpar(f,m,0.5)[1330:1700],(540,185)),cv2.resize(limpar(f,m,0.375)[1330:1700],(540,185))]))
    cv2.imwrite("diag2.jpg",np.vstack(rows))

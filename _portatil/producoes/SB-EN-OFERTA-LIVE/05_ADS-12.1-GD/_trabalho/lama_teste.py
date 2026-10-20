import json, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
B={int(k):v for k,v in json.load(open("ocr_boxes.json")).items()}
lama=SimpleLama(); cap=cv2.VideoCapture("fontes/es.mp4")
def caixas(i):
    out=[]
    for j in (i-2,i,i+2,i-1,i+1):
        for b in B.get(j,[]):
            w,h=b[2]-b[0],b[3]-b[1]
            if h>62 or w<0.5*h: continue
            out.append(b[:4])
    return out
def mask_rect(f,i):
    m=np.zeros((1280,720),np.uint8)
    for x0,y0,x1,y1 in caixas(i): m[max(0,y0-12):y1+12,max(0,x0-12):x1+12]=1
    return m
def mask_txt(f,i):
    r=mask_rect(f,i); hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    txt=((hsv[...,2]>185)&((hsv[...,1]<70)|(hsv[...,1]>150))).astype(np.uint8)&r
    return cv2.dilate(txt,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(17,17)))&cv2.dilate(r,np.ones((9,9),np.uint8))
def run(f,m):
    ys=np.where(m.any(1))[0]
    if len(ys)==0: return f
    a0=max(0,ys.min()-120);a1=min(1280,ys.max()+120)
    r=lama(Image.fromarray(cv2.cvtColor(f[a0:a1],cv2.COLOR_BGR2RGB)),Image.fromarray(m[a0:a1]*255))
    o=f.copy(); o[a0:a1]=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:a1-a0,:720]; return o
ims=[]
for q in [225,360,415,810,840,900]:
    cap.set(1,q); ok,f=cap.read()
    a=run(f,mask_rect(f,q)); b=run(f,mask_txt(f,q))
    ims.append(np.vstack([cv2.resize(x[650:1150],(240,167)) for x in (f,a,b)]))
cv2.imwrite("folhas/lama_teste.jpg",np.hstack(ims))

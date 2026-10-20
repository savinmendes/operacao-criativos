"""LaMa (GPU) no 04.mp4: legenda PT amarela (y 850-965, máscara justa: glifo + contorno, dilatada 9)
e setas vermelhas do original (quadros >= 2100, x 250-470, y 990-1200, seta + brilhos brancos).
Salva a faixa y 840-1210 em _tmp/lama/NNNN.png e as máscaras em _tmp/mask.npy. Uso: python lama04.py a b"""
import os, sys, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
torch.set_num_threads(4)
from PIL import Image
from simple_lama_inpainting import SimpleLama
R0,R1=840,1210; C0,C1=760,1240; N=2493
a,b=int(sys.argv[1]),int(sys.argv[2])
lama=SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
cap=cv2.VideoCapture('../../../UNICOS_HD/04.mp4'); cap.set(1,a)
os.makedirs('_tmp/mask',exist_ok=True); t0=time.time()
for i in range(a,b):
    ok,f=cap.read()
    if not ok: break
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
    m=np.zeros((1280,720),np.uint8)
    # legenda
    Y0,Y1=850,965
    hh,ss,vv=h[Y0:Y1],s[Y0:Y1],v[Y0:Y1]
    core=((hh>=15)&(hh<=42)&(ss>=80)&(vv>=140)).astype(np.uint8)&cv2.dilate((vv<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=cv2.morphologyEx(core,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(cv2.dilate(core,np.ones((15,15),np.uint8)))
    keep=np.zeros_like(core)
    for k in range(1,n):
        if st[k,4]>=120: keep[lab==k]=1
    core&=keep
    out=(vv<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    mm=cv2.dilate(cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))|out,np.ones((9,9),np.uint8))
    m[Y0:Y1]=mm
    # setas
    if i>=2100:
        X0,X1,Z0,Z1=250,470,985,1205
        hh,ss,vv=h[Z0:Z1,X0:X1],s[Z0:Z1,X0:X1],v[Z0:Z1,X0:X1]
        red=(((hh<=8)|(hh>=172))&(ss>=120)&(vv>=100)).astype(np.uint8)
        nr,labr,str_,_=cv2.connectedComponentsWithStats(cv2.dilate(red,np.ones((5,5),np.uint8)))
        if nr>1:
            kk=1+int(np.argmax(str_[1:,4]))
            if str_[kk,4]>800:
                cnt,_=cv2.findContours((labr==kk).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cv2.fillPoly(red,[cv2.convexHull(np.vstack(cnt))],1)
        wht=((ss<70)&(vv>=200)).astype(np.uint8)
        am=cv2.dilate(red,np.ones((11,11),np.uint8))|cv2.dilate(wht,np.ones((9,9),np.uint8))
        m[Z0:Z1,X0:X1]|=am
    np.save(f'_tmp/mask/{i:04d}.npy',m[R0:R1])
    o=f'_tmp/lama/{i:04d}.png'
    if m.sum()==0: cv2.imwrite(o,f[R0:R1]); continue
    crop=f[C0:C1].copy(); mk=m[C0:C1]
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    cv2.imwrite(o,r[R0-C0:R1-C0])
    if (i-a+1)%200==0:
        el=time.time()-t0; k=i-a+1; print(f"[{k}/{b-a}] {100*k//(b-a)}% falta ~{el/k*(b-a-k):.0f} s",flush=True)
print("ok",a,b,time.time()-t0)

"""LaMa (GPU) no 06.mp4 (24 fps): legenda PT amarela (y 965-1080, máscara justa: glifo + contorno, dilatada 9)
e setas vermelhas do original (quadros >= 1820, caixa x 250-470, y 750-985): seta vermelha + brilhos brancos que
piscam (branco que não está na mediana de ±6 quadros, para não apagar a corda branca).
Salva a faixa y 740-1090 em _tmp/lama/NNNN.png e a máscara em _tmp/mask/NNNN.npy. Uso: python lama06.py a b"""
import os, sys, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
torch.set_num_threads(4)
from PIL import Image
from simple_lama_inpainting import SimpleLama
R0,R1=740,1090; C0,C1=660,1170
a,b=int(sys.argv[1]),int(sys.argv[2])
X0,X1,Z0,Z1=250,470,750,985
lama=SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
cap=cv2.VideoCapture('../../../UNICOS_HD/06.mp4'); ini=max(0,a-6); cap.set(1,ini)
win={}; t0=time.time(); j=ini
def ler_ate(k):
    global j
    while j<=k:
        ok,f=cap.read()
        if not ok: return
        win[j]=f; j+=1
for i in range(a,b):
    ler_ate(i+6)
    if i not in win: break
    f=win[i]
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
    m=np.zeros((1280,720),np.uint8)
    Y0,Y1=965,1080
    hh,ss,vv=h[Y0:Y1],s[Y0:Y1],v[Y0:Y1]
    core=((hh>=15)&(hh<=42)&(ss>=80)&(vv>=140)).astype(np.uint8)&cv2.dilate((vv<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=cv2.morphologyEx(core,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(cv2.dilate(core,np.ones((15,15),np.uint8)))
    keep=np.zeros_like(core)
    for k in range(1,n):
        if st[k,4]>=120: keep[lab==k]=1
    core&=keep
    out=(vv<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    m[Y0:Y1]=cv2.dilate(cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))|out,np.ones((9,9),np.uint8))
    if i>=1820:
        hh,ss,vv=h[Z0:Z1,X0:X1],s[Z0:Z1,X0:X1],v[Z0:Z1,X0:X1]
        red=(((hh<=8)|(hh>=172))&(ss>=120)&(vv>=100)).astype(np.uint8)
        nr,labr,str_,_=cv2.connectedComponentsWithStats(cv2.dilate(red,np.ones((5,5),np.uint8)))
        if nr>1:
            kk=1+int(np.argmax(str_[1:,4]))
            if str_[kk,4]>800:
                cnt,_=cv2.findContours((labr==kk).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cv2.fillPoly(red,[cv2.convexHull(np.vstack(cnt))],1)
        viz=[win[k][Z0:Z1,X0:X1] for k in range(i-6,i+7) if k in win and k!=i]
        med=np.median(np.stack([cv2.cvtColor(x,cv2.COLOR_BGR2HSV)[...,2] for x in viz]),0)
        wht=((ss<70)&(vv>=200)&(vv-med>45)).astype(np.uint8)
        wht=cv2.morphologyEx(wht,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
        m[Z0:Z1,X0:X1]|=cv2.dilate(red,np.ones((11,11),np.uint8))|cv2.dilate(wht,np.ones((9,9),np.uint8))
    np.save(f'_tmp/mask/{i:04d}.npy',m[R0:R1])
    o=f'_tmp/lama/{i:04d}.png'
    if m.sum()==0: cv2.imwrite(o,f[R0:R1])
    else:
        crop=f[C0:C1].copy(); mk=m[C0:C1]
        r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
        r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
        cv2.imwrite(o,r[R0-C0:R1-C0])
    win.pop(i-7,None)
    if (i-a+1)%200==0:
        el=time.time()-t0; k=i-a+1; print(f"[{k}/{b-a}] {100*k//(b-a)}% falta ~{el/k*(b-a-k):.0f} s",flush=True)
print("ok",a,b,time.time()-t0)

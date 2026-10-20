"""LaMa (GPU) na legenda PT do gancho do 02 (quadros 0-285, faixa y 845-945). Mascara justa: glifo amarelo + contorno escuro, dilatados 9 px.
Salva a faixa y 820-970 preenchida em _tmp/lama/NNNN.png e as mascaras em _tmp/lama_mask.npy."""
import os, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
Y0,Y1=845,945; R0,R1=820,970; C0,C1=700,1110; N=286
os.makedirs('_tmp/lama',exist_ok=True)
lama=SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
cap=cv2.VideoCapture('../../../UNICOS_HD/02.mp4'); MK=np.zeros((N,R1-R0,720),np.uint8); t0=time.time()
for i in range(N):
    ok,f=cap.read(); roi=f[Y0:Y1]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    core=((h>=15)&(h<=42)&(s>=80)&(v>=140)).astype(np.uint8)&cv2.dilate((v<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    out=(v<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    m=cv2.dilate(cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))|out,np.ones((9,9),np.uint8))
    MK[i,Y0-R0:Y1-R0]=m
    o=f'_tmp/lama/{i:04d}.png'
    if m.sum()==0: cv2.imwrite(o,f[R0:R1]); continue
    crop=f[C0:C1].copy(); mk=np.zeros(crop.shape[:2],np.uint8); mk[Y0-C0:Y1-C0]=m
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    cv2.imwrite(o,r[R0-C0:R1-C0])
    if (i+1)%50==0: print(f"[{i+1}/{N}] falta ~{(time.time()-t0)/(i+1)*(N-i-1):.0f} s",flush=True)
np.save('_tmp/lama_mask.npy',MK); print("ok", time.time()-t0)

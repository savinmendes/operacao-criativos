"""LaMa (GPU) na faixa da legenda PT (y 960-1090) do 05.mp4, quadros originais 0..2367.
Máscara JUSTA = glifo amarelo + contorno escuro (dilatado 9), limitada à caixa da legenda dilatada 15 (v2; a caixa inteira borrava a corda). Salva faixa y 940-1110 em _fix/lama/NNNN.png
e a máscara em _fix/lama_mask.npy (mesmas linhas)."""
import os, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
Y0,Y1=960,1090; R0,R1=940,1110; C0,C1=820,1230; N=2368
BM=np.load('_tmp/boxmasks.npy',mmap_mode='r')
lama=SimpleLama(); print("device", lama.device if hasattr(lama,'device') else '?', torch.cuda.is_available(), flush=True)
cap=cv2.VideoCapture('../../../UNICOS_HD/05.mp4'); MK=np.zeros((N,R1-R0,720),np.uint8); t0=time.time()
for i in range(N):
    ok,f=cap.read(); roi=f[Y0:Y1]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    core=((h>=15)&(h<=42)&(s>=80)&(v>=140)).astype(np.uint8)&cv2.dilate((v<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    out=(v<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    m=cv2.dilate(cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))|out,np.ones((9,9),np.uint8))
    m&=cv2.dilate(np.array(BM[i]),np.ones((15,15),np.uint8))
    MK[i,Y0-R0:Y1-R0]=m
    out=f'_fix/lama/{i:04d}.png'
    if m.sum()==0: cv2.imwrite(out,f[R0:R1]); continue
    crop=f[C0:C1].copy(); mk=np.zeros(crop.shape[:2],np.uint8); mk[Y0-C0:Y1-C0]=m
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    cv2.imwrite(out,r[R0-C0:R1-C0])
    if (i+1)%200==0:
        el=time.time()-t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s",flush=True)
np.save('_fix/lama_mask.npy',MK); print("ok", time.time()-t0)

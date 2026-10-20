# Remove o texto ES queimado (legenda, título do gancho e texto da faixa do CTA) com LaMa na GPU, 1080x1920.
# Máscara = caixas do OCR (quadro +-2) com margem + retângulo do título nos quadros do gancho. Setas amarelas ficam.
import json, time, subprocess, warnings, sys; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
from comum3 import quadros, ENC_VF, ENC_TAG
W,H=1080,1920
B={int(k):v for k,v in json.load(open("ocr_boxes.json")).items()}
EXTRA=json.load(open("mask_extra.json"))   # [[q0,q1,x0,y0,x1,y1],...]
N=max(B)+1; PX,PY=22,20
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-",*ENC_VF,
    "-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,"base_limpa.mp4"],stdin=subprocess.PIPE)
def caixas(i):
    out=[]
    for j in (i-2,i-1,i,i+1,i+2):
        for b in B.get(j,[]):
            w,h=b[2]-b[0],b[3]-b[1]
            if h>115 or w<1.1*h or not (1150<(b[1]+b[3])/2<1600): continue   # setas / ruído / objetos da cena
            out.append(b)
    return out
ema=None; prev=None; t0=time.time(); MK=[]
for i,f in enumerate(quadros("fontes/es.mp4",w=W,h=H)):
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>18: ema=None
    prev=g
    m=np.zeros((H,W),np.uint8)
    for x0,y0,x1,y1 in caixas(i): m[max(0,y0-PY):y1+PY, max(0,x0-PX):min(W,x1+PX)]=1
    for q0,q1,x0,y0,x1,y1 in EXTRA:
        if q0<=i<q1: m[y0:y1,x0:x1]=1
    MK.append(np.packbits(m))
    if m.sum()==0:
        ema=None; enc.stdin.write(f.tobytes()); continue
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-160); a1=min(H,ys.max()+160)
    crop=f[a0:a1]; r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(m[a0:a1]*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    l=f.astype(np.float32).copy(); l[a0:a1]=r
    ema=l if ema is None else 0.8*l+0.2*ema
    al=np.maximum(cv2.GaussianBlur(m.astype(np.float32),(21,21),0),m)[...,None]
    o=np.clip(ema*al+f*(1-al),0,255).astype(np.uint8)
    enc.stdin.write(o.tobytes())
    if (i+1)%100==0: print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{(time.time()-t0)/(i+1)*(N-i-1):.0f}s",flush=True)
enc.stdin.close(); enc.wait(); np.save("base_limpa_mask.npy",np.array(MK)); print("ok",i+1)

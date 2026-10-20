# Remove a legenda ES queimada com LaMa (GPU) usando as caixas do OCR (passo 2 -> união com vizinhos), sem tocar nas setas.
import json, time, subprocess, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
from comum3 import quadros, ENC_VF, ENC_TAG
B=json.load(open("ocr_boxes.json",encoding="utf-8")); B={int(k):v for k,v in B.items()}
N=945; PX,PY=16,16
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",*ENC_VF,
    "-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,"base_limpa.mp4"],stdin=subprocess.PIPE)
def caixas(i):
    out=[]
    for j in (i-2,i,i+2,i-1,i+1):
        for b in B.get(j,[]):
            w,h=b[2]-b[0],b[3]-b[1]
            if h>62 or w<0.5*h: continue   # seta/ruído: só caixas de linha de legenda
            out.append(b[:4])
    return out
ema=None; prev=None; t0=time.time(); MK=[]
for i,f in enumerate(quadros("fontes/es.mp4")):
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>20: ema=None
    prev=g
    m=np.zeros((1280,720),np.uint8)
    if 618<=i<=670: m[735:818,560:645]=1   # 'Y' solto que o detector não pega
    for x0,y0,x1,y1 in caixas(i): m[max(0,y0-PY):y1+PY, max(0,x0-PX):x1+PX]=1
    MK.append(np.packbits(m))
    if m.sum()==0:
        ema=None; enc.stdin.write(f.tobytes()); continue
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(1280,ys.max()+120)
    crop=f[a0:a1]; r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(m[a0:a1]*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    l=f.astype(np.float32).copy(); l[a0:a1]=r
    ema=l if ema is None else 0.85*l+0.15*ema
    al=np.maximum(cv2.GaussianBlur(m.astype(np.float32),(15,15),0),m)[...,None]
    o=np.clip(ema*al+f*(1-al),0,255).astype(np.uint8)
    enc.stdin.write(o.tobytes())
    if (i+1)%100==0: print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{(time.time()-t0)/(i+1)*(N-i-1):.0f}s",flush=True)
enc.stdin.close(); enc.wait(); np.save("base_limpa_mask.npy",np.array(MK)); print("ok",i+1)

# Remove a legenda ES (caixas do OCR, uniao com quadros vizinhos, +pad) e a seta vermelha do CTA com LaMa (GPU).
# Leitura/gravacao com matriz bt601/tv fixa (armadilha da cor). Saida: base_limpa.mp4 (sem audio).
import json, time, subprocess, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
W,H,FPS=720,1280,30
SRC="../original/SB-ES_ADS-12.18.mp4"
B={int(k):[b for b in v if 20<=b[3]-b[1]<=72 and b[2]-b[0]>=60] for k,v in json.load(open("ocr_boxes.json")).items()}
N=945; PAD=12; SETA_DE=int(26.05*FPS); SX0,SY0,SX1,SY1=230,560,500,980
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
    "-f","rawvideo","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
    "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
    "base_limpa.mp4"],stdin=subprocess.PIPE)
def mascara(i,f):
    m=np.zeros((H,W),np.uint8)
    for j in (i//5*5-5,i//5*5,i//5*5+5):
        for x0,y0,x1,y1 in B.get(j,[]):
            if i>=152:  # fora do gancho a legenda e centrada: espelha a caixa no centro e alarga 40 px (pega o "Y" solto que o OCR perde)
                x0,x1=min(x0,W-x1)-40,max(x1,W-x0)+40
            m[max(0,y0-PAD):y1+PAD, max(0,x0-PAD):min(W,x1+PAD)]=1
    if i>=SETA_DE:
        hsv=cv2.cvtColor(f[SY0:SY1,SX0:SX1],cv2.COLOR_BGR2HSV)
        red=(((hsv[...,0]<9)|(hsv[...,0]>170))&(hsv[...,1]>150)&(hsv[...,2]>110)).astype(np.uint8)
        n,lab,st,_=cv2.connectedComponentsWithStats(red)
        keep=np.zeros_like(red)
        for k in range(1,n):
            if st[k,cv2.CC_STAT_AREA]>=150: keep[lab==k]=1
        m[SY0:SY1,SX0:SX1]|=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
    return m
prev=None; ema=None; t0=time.time(); MK=[]
for i in range(N):
    raw=dec.stdout.read(W*H*3)
    if len(raw)<W*H*3: break
    f=np.frombuffer(raw,np.uint8).reshape(H,W,3).copy()
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>20: ema=None
    prev=g
    m=mascara(i,f); MK.append(np.packbits(m))
    if m.sum()==0:
        ema=None; enc.stdin.write(f.tobytes()); continue
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(H,ys.max()+120)
    crop=f[a0:a1]; mk=m[a0:a1]
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    l=f.astype(np.float32).copy(); l[a0:a1]=r
    ema=l if ema is None else 0.6*l+0.4*ema
    al=np.maximum(cv2.GaussianBlur(m.astype(np.float32),(15,15),0),m)[...,None]
    out=np.clip(ema*al+f*(1-al),0,255).astype(np.uint8)
    enc.stdin.write(out.tobytes())
    if (i+1)%100==0:
        el=time.time()-t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s",flush=True)
enc.stdin.close(); enc.wait(); np.save("base_limpa_mask.npy",np.array(MK)); print("ok",time.time()-t0)

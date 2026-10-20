# LaMa GPU: tira legenda ES (gancho Jesus + ceu). Saida base_limpa.mp4 (720x1280, bt601/tv fixo)
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
sys.path.insert(0,'.')
from mascara import mascara
SRC=r"C:\Users\PICHAU\Downloads\1-VIDEOS\ad 20.mp4"; W,H=720,1280; HOOKF=128
def quadros():
    p=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-an",
  "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
  "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","smpte170m","base_limpa.mp4"],stdin=subprocess.PIPE)
ema=None; prev=None; t0=time.time(); N=4235
for i,f in enumerate(quadros()):
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>20: ema=None
    prev=g
    m=mascara(f,hook=i<HOOKF)
    if m.sum()==0:
        ema=None; ff.stdin.write(f.tobytes()); continue
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(H,ys.max()+120)
    crop=f[a0:a1]; mk=m[a0:a1]
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    l=f.astype(np.float32).copy(); l[a0:a1]=r
    ema=l if ema is None else 0.65*l+0.35*ema
    al=np.maximum(cv2.GaussianBlur(m.astype(np.float32),(11,11),0),m)[...,None]
    o=np.clip(ema*al+f*(1-al),0,255).astype(np.uint8)
    ff.stdin.write(o.tobytes())
    if (i+1)%300==0:
        el=time.time()-t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s",flush=True)
ff.stdin.close(); ff.wait(); print("ok",i+1,round(time.time()-t0))

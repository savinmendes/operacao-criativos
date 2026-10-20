# v2: mascara em faixa (uniao temporal +-4 quadros, simetrica no centro), setas com halo; LaMa GPU
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
sys.path.insert(0,'.')
from mascara import mascara
SRC="src.mp4"; W,H=720,1280; HOOKF=127; S0,S1=3870,4100
def quadros():
    p=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
def setas(f):
    hs=cv2.cvtColor(f[960:],cv2.COLOR_BGR2HSV); h,s,v=[hs[...,i].astype(int) for i in range(3)]
    r=(((h<=12)|(h>=160))&(s>=55)&(v>=110)).astype(np.uint8)
    r=cv2.morphologyEx(r,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(r); mm=np.zeros_like(r)
    for k in range(1,n):
        if st[k][4]>=250: mm|=(lab==k).astype(np.uint8)
    mm=cv2.dilate(mm,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(31,31)))
    o=np.zeros((H,W),np.uint8); o[960:]=mm; return o
# passada 1: caixas por quadro
caixas=[]; ms_hook={}; ms_set={}
for i,f in enumerate(quadros()):
    if i<HOOKF:
        m=mascara(f,hook=True); ms_hook[i]=m; caixas.append(None); continue
    m=mascara(f)
    if S0<=i<=S1: ms_set[i]=setas(f)
    if m.sum()==0: caixas.append(None); continue
    ys,xs=np.where(m>0); hw=max(360-xs.min(),xs.max()-360)
    caixas.append((ys.min(),ys.max(),hw))
N=len(caixas); print("passada1",N,flush=True)
def mask_i(i):
    if i<HOOKF: return ms_hook[i]
    c=[caixas[j] for j in range(max(HOOKF,i-4),min(N,i+5)) if caixas[j] is not None]
    m=np.zeros((H,W),np.uint8)
    if caixas[i] is not None or len(c)>=2:
        if c:
            y0=min(x[0] for x in c)-14; y1=max(x[1] for x in c)+18; hw=max(x[2] for x in c)+30
            m[max(0,y0):min(H,y1),max(0,360-hw):min(W,360+hw)]=1
    if i in ms_set: m|=ms_set[i]
    return m
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-an",
  "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
  "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","smpte170m","base_limpa.mp4"],stdin=subprocess.PIPE)
t0=time.time()
for i,f in enumerate(quadros()):
    m=mask_i(i)
    if m.sum()==0: ff.stdin.write(f.tobytes()); continue
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(H,ys.max()+120)
    crop=f[a0:a1]; mk=m[a0:a1]
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    al=np.maximum(cv2.GaussianBlur(mk.astype(np.float32),(15,15),0),mk)[...,None]
    o=f.copy(); o[a0:a1]=np.clip(r*al+crop*(1-al),0,255).astype(np.uint8)
    ff.stdin.write(o.tobytes())
    if (i+1)%300==0:
        el=time.time()-t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s",flush=True)
ff.stdin.close(); ff.wait(); print("ok",i+1,round(time.time()-t0))

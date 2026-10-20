# Refaz quadros 2030-2160 (legenda sobre o prédio escuro): máscara estendida até a borda direita
import sys, warnings, subprocess; warnings.filterwarnings("ignore")
import numpy as np, cv2
from PIL import Image
from simple_lama_inpainting import SimpleLama
from mascara2 import mascara
SRC=r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"
W,H=1080,1920; A,B=2030,2160
lama=SimpleLama()
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf",f"select='between(n,{A},{B-1})',scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-fps_mode","passthrough","-f","rawvideo","-"],stdout=subprocess.PIPE)
out=[]
for i in range(A,B):
    raw=dec.stdout.read(W*H*3); f=np.frombuffer(raw,np.uint8).reshape(H,W,3).copy()
    m=mascara(f)
    # faixa da legenda: linhas onde há máscara -> retângulo do x mínimo até a borda direita
    rows=np.where(m.any(1))[0]
    if len(rows):
        y0,y1=rows.min(),rows.max(); x0=np.where(m.any(0))[0].min()
        m[y0:y1+1,x0:]=1
    else:
        m[1420:1580,100:]=1
    ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(H,ys.max()+120)
    crop=f[a0:a1]; mk=m[a0:a1]
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
    al=np.maximum(cv2.GaussianBlur(mk.astype(np.float32),(15,15),0),mk)[...,None]
    f[a0:a1]=np.clip(r*al+crop*(1-al),0,255).astype(np.uint8)
    out.append(f)
np.save("patch_2030_2160.npy",np.stack(out)); print("ok",len(out))

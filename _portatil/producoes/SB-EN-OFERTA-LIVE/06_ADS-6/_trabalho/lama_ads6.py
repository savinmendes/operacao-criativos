# Remove a legenda queimada ES (faixa inferior) com LaMa na GPU; leitura/gravação com matriz bt601/tv fixa
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import numpy as np, cv2, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
from mascara2 import mascara
SRC=r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"
W,H=1080,1920; FPS=30
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an",
    "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p","-c:v","libx264","-crf","12","-preset","medium",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1","base_limpa.mp4"],stdin=subprocess.PIPE)
N=4107; i=0; t0=time.time(); ema=None
while True:
    raw=dec.stdout.read(W*H*3)
    if len(raw)<W*H*3: break
    f=np.frombuffer(raw,np.uint8).reshape(H,W,3).copy()
    m=mascara(f)
    if m.any():
        ys=np.where(m.any(1))[0]; a0=max(0,ys.min()-120); a1=min(H,ys.max()+120)
        crop=f[a0:a1]; mk=m[a0:a1]
        r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
        r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]].astype(np.float32)
        al=np.maximum(cv2.GaussianBlur(mk.astype(np.float32),(15,15),0),mk)[...,None]
        f[a0:a1]=np.clip(r*al+crop*(1-al),0,255).astype(np.uint8)
    enc.stdin.write(f.tobytes()); i+=1
    if i%150==0:
        el=time.time()-t0; print(f"[{i}/{N}] {100*i//N}% falta ~{el/i*(N-i):.0f} s",flush=True)
enc.stdin.close(); enc.wait(); print("ok",i,round(time.time()-t0))

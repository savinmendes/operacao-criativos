# Compoe o AD PL (leitura sequencial p/ pouca RAM): A/F = lipsync HeyGen (entrada = base limpa + audio ES original),
# remendado com a base limpa 3 na faixa da antiga legenda; B-E = base limpa 3 (E a ~0,92x); legenda PL + mix
import numpy as np, subprocess, json, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_TAG
import cv2
W,H,FPS=720,1280,30
CJ=json.load(open("cortes_pl.json")); C,ES=CJ["C"],CJ["ES"]; TOTAL=C[-1]
BASE=sys.argv[3] if len(sys.argv)>3 else "lama/base_limpa2.mp4"
A=sys.argv[1] if len(sys.argv)>1 else "heygen/A_heygen.mp4"; F=sys.argv[2] if len(sys.argv)>2 else "heygen/F_heygen.mp4"
FSLOW=5.70/5.40
class Seq:
    def __init__(s,p): s.g=quadros(p); s.c={}; s.n=-1; s.last=None
    def get(s,i):
        while s.n<i:
            f=next(s.g,None)
            if f is None: return s.c.get(s.n)
            s.n+=1; s.c[s.n]=f
            for k in [k for k in s.c if k<s.n-3]: del s.c[k]
        return s.c.get(i, s.c[min(s.c)])
base=Seq(BASE); fa=Seq(A); ff=Seq(F)
M1=np.load("lama/mask_v1.npy"); M2=np.load("lama/mask.npy")
def mk(i):
    m=(np.unpackbits(M1[i])[:H*W].reshape(H,W)|np.unpackbits(M2[i])[:H*W].reshape(H,W)).astype(np.uint8)
    m=cv2.dilate(m,np.ones((15,15),np.uint8)).astype(np.float32); return cv2.GaussianBlur(m,(0,0),5)[...,None]
def dcor(img,b):
    # desvio de cor HeyGen x base (regiao fora do rosto, metade de baixo)
    return (b[700:1250].astype(np.float32)-img[700:1250].astype(np.float32)).mean(axis=(0,1))
DV={}
def remenda(img,i,key):
    i=min(i,944); b=base.get(i); m=mk(i)
    if key not in DV: DV[key]=dcor(img,b); print("desvio cor",key,DV[key])
    img=np.clip(img.astype(np.float32)+DV[key],0,255)
    return np.clip(b*m+img*(1-m),0,255).astype(np.uint8)
N=int(round(TOTAL*FPS))
vf=("[0:v]scale=1080:1920:flags=lanczos,ass=leg_pl.ass:fontsdir=fonts,"
    "scale=720:1280:flags=lanczos:out_color_matrix=bt601:out_range=tv,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
     "-i","audio/mix_pl.wav","-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","17","-preset","medium",
     *ENC_TAG,"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}","-movflags","+faststart","bruto_pl.mp4"],stdin=subprocess.PIPE)
def pega(seq,x):
    j=int(np.floor(x)); a=x-j; f0=seq.get(j)
    if a<0.05: return f0
    return cv2.addWeighted(f0,1-a,seq.get(j+1),a,0)
for n in range(N):
    t=n/FPS; k=max(i for i in range(6) if C[i]<=t+1e-6); u=t-C[k]
    if k==0: img=remenda(fa.get(n),n,"A")
    elif k==5:
        j=int(round(u*FPS)); img=remenda(ff.get(j),783+int(round(j/FSLOW)),"F")
    elif k==4:
        sp=min(1.0,(ES[5]-ES[4]-0.05)/(C[5]-C[4])); img=pega(base,(ES[4]+u*sp)*FPS)
    else: img=pega(base,(ES[k]+u)*FPS)
    enc.stdin.write(np.ascontiguousarray(img).tobytes())
enc.stdin.close(); enc.wait(); print("ok bruto_pl.mp4",N)

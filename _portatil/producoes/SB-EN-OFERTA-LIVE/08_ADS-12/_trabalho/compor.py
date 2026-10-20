# Compoe o AD EN: cena A/F = lipsync HeyGen sobre base sem legenda; B-E = base sem legenda (E em 0,9x); legenda EN + mix
import numpy as np, subprocess, json, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
import cv2
W,H,FPS=720,1280,30
CJ=json.load(open("cortes_en.json")); C,ES=CJ["C"],CJ["ES"]; TOTAL=C[-1]
BASE="lama/base_limpa2.mp4"
A=sys.argv[1] if len(sys.argv)>1 else "heygen/A_heygen.mp4"; F=sys.argv[2] if len(sys.argv)>2 else "heygen/F_heygen.mp4"
def ler(p,ini,n):
    return list(quadros(p,int(round(ini*FPS)),n))
base=list(quadros(BASE))
M1=np.load("lama/mask_v1.npy"); M2=np.load("lama/mask.npy")
def mk(i):
    m=(np.unpackbits(M1[i])[:H*W].reshape(H,W)|np.unpackbits(M2[i])[:H*W].reshape(H,W)).astype(np.uint8)
    m=cv2.dilate(m,np.ones((15,15),np.uint8)).astype(np.float32); return cv2.GaussianBlur(m,(0,0),5)[...,None]
def remenda(img,i):
    i=min(i,len(base)-1); m=mk(i)
    return np.clip(base[i]*m+img*(1-m),0,255).astype(np.uint8)
fa=ler(A,0,400); ff=ler(F,0,400)
print("frames base",len(base),"A",len(fa),"F",len(ff))
N=int(round(TOTAL*FPS))
vf=("[0:v]scale=1080:1920:flags=lanczos,ass=leg_en.ass:fontsdir=fonts,"
    "scale=720:1280:flags=lanczos:out_color_matrix=bt601:out_range=tv,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
     "-i","audio/mix_en.wav","-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","17","-preset","medium",
     *ENC_TAG,"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}","-movflags","+faststart","bruto_en.mp4"],stdin=subprocess.PIPE)
def pega(lst,x):
    j=int(np.floor(x)); a=x-j; j=min(max(j,0),len(lst)-1); j2=min(j+1,len(lst)-1)
    return lst[j] if a<0.05 or j==j2 else cv2.addWeighted(lst[j],1-a,lst[j2],a,0)
for n in range(N):
    t=n/FPS; k=max(i for i in range(6) if C[i]<=t+1e-6); u=t-C[k]
    if k==0: img=remenda(pega(fa,u*FPS),int(round(u*FPS)))
    elif k==5: img=remenda(pega(ff,u*FPS),783+int(round(u*FPS)))
    elif k==4:
        sp=min(1.0,(ES[5]-ES[4]-0.05)/(C[5]-C[4])); img=pega(base,(ES[4]+u*sp)*FPS)
    else: img=pega(base,(ES[k]+u)*FPS)
    enc.stdin.write(np.ascontiguousarray(img).tobytes())
enc.stdin.close(); enc.wait(); print("ok bruto_en.mp4",N)

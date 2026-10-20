"""Remove legenda amarela queimada (faixa y 960-1090) de 05.mp4, quadros 0..2367 (até o fim da Desatadora).
Câmera fixa: placa temporal (mediana dos pixels fora da caixa) por tomada; quadros com movimento na faixa: LaMa local.
Saída: _tmp/semleg_orig.mp4 (24 fps, tempo ORIGINAL, sem áudio)."""
import subprocess, warnings, cv2, numpy as np
from PIL import Image
warnings.filterwarnings("ignore")
SRC='../../../UNICOS_HD/05.mp4'; OUT='_tmp/semleg_orig.mp4'
Y0,Y1=960,1090; N=2368
SHOTS=[0,75,87,161,196,286,653,1271,1366,1372,N]
def txtmask(roi):
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    yel=((h>=18)&(h<=40)&(s>=100)&(v>=160)).astype(np.uint8)
    yel&=cv2.dilate((v<80).astype(np.uint8),np.ones((7,7),np.uint8))
    return yel
cap=cv2.VideoCapture(SRC); F=[]
for i in range(N):
    ok,f=cap.read(); F.append(f)
BM=[]
for i in range(N):
    t=txtmask(F[i][Y0:Y1]); m=np.zeros(t.shape,np.uint8)
    for ya,yb in [(0,72),(66,130)]:
        ys,xs=np.nonzero(t[ya:yb])
        if len(xs)>40:
            x0,x1=np.percentile(xs,0.5),np.percentile(xs,99.5); y0,y1=np.percentile(ys,0.5)+ya,np.percentile(ys,99.5)+ya
            m[max(0,int(y0)-9):int(y1)+11, max(0,int(x0)-12):int(x1)+14]=1
    BM.append(m)
BM=np.stack(BM); np.save('_tmp/boxmasks.npy',BM)
print("caixas ok; quadros com legenda:", int((BM.reshape(N,-1).max(1)>0).sum()), flush=True)
shot_of=np.zeros(N,int)
for k in range(len(SHOTS)-1): shot_of[SHOTS[k]:SHOTS[k+1]]=k
from simple_lama_inpainting import SimpleLama
lama=SimpleLama()
def lama_faixa(f,m):
    a0,a1=Y0-140,Y1+140; crop=f[a0:a1].copy()
    mk=np.zeros(crop.shape[:2],np.uint8); mk[Y0-a0:Y1-a0]=cv2.dilate(m,np.ones((7,7),np.uint8))
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    al=cv2.GaussianBlur(mk.astype(np.float32),(9,9),0)[...,None]; al=np.maximum(al,mk[...,None].astype(np.float32))
    g=f.copy(); g[a0:a1]=np.clip(r*al+crop*(1-al),0,255).astype(np.uint8); return g
# placas por tomada
P={}
for k in range(len(SHOTS)-1):
    a,b=SHOTS[k],SHOTS[k+1]
    if b-a<20: continue
    st=np.stack([F[i][Y0:Y1] for i in range(a,b)]).astype(np.float32); mk=BM[a:b].astype(bool)
    st[mk]=np.nan; p=np.nanmedian(st,axis=0); bur=np.isnan(p).any(2); p=np.nan_to_num(p).astype(np.uint8)
    if bur.any():
        full=F[(a+b)//2].copy(); full[Y0:Y1]=p
        p=lama_faixa(full,bur.astype(np.uint8))[Y0:Y1]
    P[k]=p.astype(np.float32); print("placa",k,a,b,"buracos",int(bur.sum()),flush=True)
# movimento (pixels livres vs placa)
mov=np.full(N,99.0)
for i in range(N):
    k=shot_of[i]
    if k not in P: continue
    roi=F[i][Y0:Y1].astype(np.float32); m=cv2.dilate(BM[i],np.ones((9,9),np.uint8))
    d=np.abs(roi-P[k]).mean(2); free=(m==0)
    cols=[d[:,x:x+40][free[:,x:x+40]].mean() if free[:,x:x+40].sum()>200 else 0 for x in range(0,720,40)]
    mov[i]=max(cols)
np.save('_tmp/mov.npy',mov)
usa=np.zeros(N,bool)
for j in np.nonzero(mov>12)[0]: usa[max(0,j-6):j+7]=True
temleg=BM.reshape(N,-1).max(1)>0
print("quadros LaMa:",int((usa&temleg).sum()),flush=True)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
ema=None; prevk=-1
for i in range(N):
    f=F[i]; k=shot_of[i]; m=BM[i]
    if not temleg[i]: g=f
    elif usa[i] or k not in P:
        g=lama_faixa(f,m)
    else:
        roi=f[Y0:Y1]; p=P[k]
        anel=(cv2.dilate(m,np.ones((21,21),np.uint8))>0)&(m==0)
        if anel.sum()>50: p=p+(roi[anel].astype(np.float32).mean(0)-p[anel].mean(0))
        al=cv2.GaussianBlur(cv2.dilate(m,np.ones((9,9),np.uint8)).astype(np.float32),(15,15),0)[...,None]
        al=np.maximum(al,m[...,None].astype(np.float32))
        g=f.copy(); g[Y0:Y1]=np.clip(p*al+roi*(1-al),0,255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(g).tobytes())
    if i%120==0: print(f"[{i}/{N}] {100*i//N}%",flush=True)
ff.stdin.close(); ff.wait(); print("ok",OUT)

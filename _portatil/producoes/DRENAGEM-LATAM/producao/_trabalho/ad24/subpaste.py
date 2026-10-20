# Cola a caixa de legenda (branca, texto preto) de um quadro de referência sobre um intervalo, cobrindo a legenda errada.
import cv2,numpy as np,subprocess,sys
ent,sai=sys.argv[1],sys.argv[2]; jobs=[tuple(map(float,j.split(":"))) for j in sys.argv[3:]]  # de:ate:ref
Y0,Y1=860,1120
cap=cv2.VideoCapture(ent); W,H=int(cap.get(3)),int(cap.get(4)); N=int(cap.get(7))
def caixa(f):
    g=f[Y0:Y1]; m=(g.min(axis=2)>225).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,25),np.uint8))
    k,lab,st,_=cv2.connectedComponentsWithStats(m); out=np.zeros_like(m)
    for i in range(1,k):
        x,y,w,h,a=st[i]
        if a>2000 and w>80: out[lab==i]=1
    return out
refs={}
for de,ate,ref in jobs:
    cap.set(1,int(round(ref*30))); ok,f=cap.read(); refs[ref]=(f[Y0:Y1].copy(),caixa(f))
cap.set(1,0)
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-i",ent,"-map","0:v","-map","1:a","-c:v","libx264","-crf","14","-pix_fmt","yuv420p","-c:a","copy",sai],stdin=subprocess.PIPE)
n=0;sobra=[]
while True:
    ok,f=cap.read()
    if not ok: break
    for de,ate,ref in jobs:
        if de*30-0.5<=n<ate*30-0.5:
            rp,rm=refs[ref]; old=caixa(f)
            m=np.maximum(rm,0)
            band=f[Y0:Y1]; band[m>0]=rp[m>0]
            rest=(old>0)&(m==0)
            if rest.any(): sobra.append((n,int(rest.sum())))
    p.stdin.write(f.tobytes()); n+=1
p.stdin.close(); p.wait(); print("ok",n,"sobras(px):",sobra[:5],len(sobra))

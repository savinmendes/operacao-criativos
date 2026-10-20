import cv2, numpy as np, sys
from config_v2 import OLD, V2
def q(p):
    c=cv2.VideoCapture(str(p)); r=[]
    while True:
        ok,im=c.read()
        if not ok: break
        r.append(im)
    return r
rows=[]
for ad,clip in [("ad14","flora2/t6_final.mp4"),("ad10","flora2/t4p_final.mp4"),("ad22","flora/t1_final.mp4"),("ad04","flora/r2_final.mp4"),("ad19","flora/t2_final.mp4"),("ad16","flora/t1_final.mp4")]:
    a=q(OLD/ad/clip); fx=V2/ad/clip; b=q(fx.with_name(fx.stem+"_fixcheck.mp4"))
    H=a[0].shape[0]; best=(-1,0)
    cnts=[]
    for i,(x,y) in enumerate(zip(a,b)):
        d=(np.abs(x.astype(int)-y.astype(int)).max(2)>40); d[int(H*.62):int(H*.9)]=0
        cnts.append(int(d.sum()))
    i=int(np.argsort(cnts)[len(cnts)//2]) if ad=="ad19" else int(np.argmax(cnts))
    for i in sorted({int(np.argmax(cnts)), int(np.argsort(cnts)[len(cnts)//2])}):
        x,y=a[i],b[i]
        d=(np.abs(x.astype(int)-y.astype(int)).max(2)>40).astype(np.uint8); d[int(H*.62):int(H*.9)]=0
        ys,xs=np.where(d)
        cy,cx=(int(np.median(ys)),int(np.median(xs))) if len(ys) else (H//2,360)
        L=200; x0=int(np.clip(cx-L//2,0,x.shape[1]-L)); y0=int(np.clip(cy-L//2,0,H-L))
        za=cv2.resize(x[y0:y0+L,x0:x0+L],None,fx=2,fy=2); zb=cv2.resize(y[y0:y0+L,x0:x0+L],None,fx=2,fy=2)
        t1=x.copy(); cv2.rectangle(t1,(x0,y0),(x0+L,y0+L),(0,255,255),3); t1=cv2.resize(t1,(225,400))
        t2=y.copy(); cv2.rectangle(t2,(x0,y0),(x0+L,y0+L),(0,255,255),3); t2=cv2.resize(t2,(225,400))
        r=np.hstack([t1,za,zb,t2]); cv2.putText(r,f"{ad} {clip} q{i} px{cnts[i]}",(5,20),0,0.6,(0,255,255),2); rows.append(r)
cv2.imwrite("_chk_naolistados.jpg",np.vstack(rows))

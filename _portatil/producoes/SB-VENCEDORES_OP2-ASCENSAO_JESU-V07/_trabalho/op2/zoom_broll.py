import cv2, numpy as np
B=r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS\\"
def rd(p,t):
    c=cv2.VideoCapture(p); c.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=c.read(); return cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
orb=cv2.ORB_create(4000); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
mask=np.zeros((1920,1080),np.uint8); mask[:1250]=255  # evita legenda/setas
def est(a,b):
    ka,da=orb.detectAndCompute(a,mask); kb,db=orb.detectAndCompute(b,None)
    m=bf.match(da,db)
    pa=np.float32([ka[x.queryIdx].pt for x in m]); pb=np.float32([kb[x.trainIdx].pt for x in m])
    M,inl=cv2.estimateAffinePartial2D(pb,pa,ransacReprojThreshold=4)
    s=np.hypot(M[0,0],M[1,0]); w=cv2.warpAffine(b,M,(1080,1920))
    d=np.abs(w[:1250].astype(float)-a[:1250]).mean()
    return s,M[0,2],M[1,2],int(inl.sum()),d
cenas=[("SB-BRV-55 MANO EN EL PECHO KLING25.mp4",7.5,8.8),("SB-BRV-01 REGALO NOMBRE KLING25.mp4",9.0,12.4),("SB-BRV-69 CATACUMBAS KLING25.mp4",12.7,16.3),("SB-BRV-03 LLUVIA MILAGROS KLING25.mp4",16.6,19.3),("SB-BRV-30 SCROLL DETENIDO KLING25.mp4",22.7,25.8)]
for f,a,b in cenas:
    print(f)
    for t in (a,b):
        A=rd(r"..\..\SB-OP2-ASCENSAO.mp4",t); best=None
        for tb in np.arange(0,5.0,0.125):
            try: r=est(A,rd(B+f,tb))
            except Exception: continue
            if best is None or r[4]<best[1][4]: best=(tb,r)
        tb,(s,tx,ty,n,d)=best
        print(f"  ad {t:.2f} br {tb:.3f} escala {s:.3f} tx {tx:.0f} ty {ty:.0f} inl {n} diff {d:.1f}")

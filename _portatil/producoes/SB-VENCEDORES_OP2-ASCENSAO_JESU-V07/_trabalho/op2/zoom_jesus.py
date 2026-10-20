import cv2, numpy as np
def rd(p,t):
    c=cv2.VideoCapture(p); c.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=c.read(); return cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
orb=cv2.ORB_create(4000); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
mask=np.zeros((1920,1080),np.uint8); mask[:1250]=255
C=r"C:\Users\PICHAU\Downloads\1-VIDEOS\SB-CORPO_CTA_COMPLETO_JESU.mp4"
H=r"C:\Users\PICHAU\Downloads\HOOKS SAO BENITO\SB-HOOK-OP2_AV30_ASCENSAO.mp4"
for src,t,off in [(H,1.0,0),(H,3.0,0),(C,4.0,3.2),(C,7.0,3.2),(C,20.0,3.2),(C,22.0,3.2),(C,27.0,3.2),(C,30.0,3.2)]:
    A=rd(r"..\..\SB-OP2-ASCENSAO.mp4",t); best=None
    for dt in np.arange(-0.2,0.21,0.04):
        b=rd(src,t-off+dt); b=cv2.resize(b,(1080,1920))
        ka,da=orb.detectAndCompute(A,mask); kb,db=orb.detectAndCompute(b,None)
        m=bf.match(da,db); pa=np.float32([ka[x.queryIdx].pt for x in m]); pb=np.float32([kb[x.trainIdx].pt for x in m])
        M,inl=cv2.estimateAffinePartial2D(pb,pa,ransacReprojThreshold=4)
        w=cv2.warpAffine(b,M,(1080,1920)); d=np.abs(w[:1250].astype(float)-A[:1250]).mean()
        d0=np.abs(b[:1250].astype(float)-A[:1250]).mean()
        if best is None or d<best[0]: best=(d,dt,np.hypot(M[0,0],M[1,0]),M[0,2],M[1,2],d0)
    print(t, "dt %.2f esc %.3f tx %.0f ty %.0f diff %.1f semwarp %.1f"%(best[1],best[2],best[3],best[4],best[0],best[5]))

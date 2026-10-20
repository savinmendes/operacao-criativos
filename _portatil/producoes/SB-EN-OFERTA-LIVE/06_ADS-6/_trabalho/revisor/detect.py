import cv2, numpy as np
V=r'C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\06_ADS-6\SB-EN-ADS-6.mp4'
cap=cv2.VideoCapture(V); i=0; out=[]
Y0,Y1=1400,1600
while True:
    ok,f=cap.read()
    if not ok: break
    if i%3==0:
        s=f[Y0:Y1].astype(np.float32); g=cv2.cvtColor(f[Y0:Y1],cv2.COLOR_BGR2GRAY).astype(np.float32)
        hsv=cv2.cvtColor(f[Y0:Y1],cv2.COLOR_BGR2HSV)
        txt=((hsv[...,1]>120)&(hsv[...,2]>150))|(g>235)|(g<40)
        txt=cv2.dilate(txt.astype(np.uint8),np.ones((25,25),np.uint8))>0
        gx=np.abs(cv2.Sobel(g,cv2.CV_32F,1,0,ksize=3)); gx[txt]=0
        e=(gx>25).astype(np.uint8)
        # longest vertical run per column
        col=e.sum(0)
        best=0;bx=0
        for x in np.where(col>50)[0]:
            c=e[:,x]; r=0;m=0
            for v in c:
                r=r+1 if v else 0; m=max(m,r)
            if m>best: best=m;bx=x
        out.append((i/30,best,bx))
    i+=1
np.save('det.npy',np.array(out))
hits=[o for o in out if o[1]>=50]
prev=None;start=None
for t,b,x in hits:
    if prev is None or t-prev>0.25:
        if start is not None: print(f'{start:.1f}-{prev:.1f}')
        start=t
    prev=t
if start is not None: print(f'{start:.1f}-{prev:.1f}')

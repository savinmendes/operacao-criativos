import cv2,numpy as np,sys
def diffs(p):
    cap=cv2.VideoCapture(p);prev=None;d=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        g=cv2.cvtColor(cv2.resize(f,(180,320)),cv2.COLOR_BGR2GRAY).astype(np.float32)[25:190]
        if prev is not None: d.append(np.abs(g-prev).mean())
        prev=g
    return np.array(d)
a=diffs('../../SB-EN-ADS-24.mp4'); b=diffs(r'C:\Users\PICHAU\Downloads\1-VIDEOS\ad 24.mp4')
np.save('dfin.npy',a);np.save('dorig.npy',b)
def rep(d,name):
    print(name)
    out=[]
    for s in range(0,len(d)//30):
        seg=d[s*30:(s+1)*30]; out.append(f"{s}:{(seg<0.35).sum()}")
    print(' '.join(out))
rep(a,'final dup frames/s'); rep(b,'orig dup frames/s')

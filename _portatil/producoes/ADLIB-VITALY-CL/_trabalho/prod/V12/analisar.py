import cv2, numpy as np, sys
V=r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4"
cap=cv2.VideoCapture(V); i=0; prev=None; prevt=None
rng=[(430,580),(1060,1450),(1900,1960)]
def ok(i): return any(a<=i<=b for a,b in rng)
while True:
    r,f=cap.read()
    if not r: break
    if ok(i):
        b=f[900:1100].astype(int); B,G,R=b[...,0],b[...,1],b[...,2]
        m=(G-R>35)&(G-B>35)&(G<170)&(R<110)
        rows=np.where(m.sum(1)>200)[0]; cols=np.where(m.sum(0)>20)[0]
        bb=(rows[0]+900,rows[-1]+900,cols[0],cols[-1]) if len(rows) and len(cols) else None
        w=(b.min(2)>225)&m.any(0)[None,:]  # white text
        sig=cv2.resize(((f[900:1100].min(2)>225)*255).astype(np.uint8),(72,20))
        t=f[30:160]; ts=cv2.resize(((t.min(2)>230)*255).astype(np.uint8),(72,13))
        if prev is not None:
            d=np.abs(sig.astype(int)-prev).mean(); dt=np.abs(ts.astype(int)-prevt).mean()
            if d>12 or dt>12: print(i, f"{i/30:.3f}", "cap" if d>12 else "", "tit" if dt>12 else "", bb)
        prev=sig.astype(int); prevt=ts.astype(int)
    i+=1

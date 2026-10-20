import cv2,numpy as np,sys
def fr(p,t):
    c=cv2.VideoCapture(p);c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read()
    return cv2.resize(f,(90,160)).astype(float)[:100] if ok else None
ref=sys.argv[1]
for src in sys.argv[2:]:
  print(src)
  for t in [0.2,1.5,3,4.5,5.8]:
    a=fr(ref,t)
    best=min(((np.abs(a-fr(src,s)).mean(),s) for s in np.arange(0,6.1,0.1) if fr(src,s) is not None))
    print(" ",t,"->",round(best[1],2),round(best[0],1))

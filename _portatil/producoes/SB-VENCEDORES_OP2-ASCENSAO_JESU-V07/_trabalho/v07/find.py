import cv2,numpy as np,glob,sys
def th(f): return cv2.resize(f,(36,64)).astype(float)[:44]
c=cv2.VideoCapture('es.mp4'); c.set(cv2.CAP_PROP_POS_MSEC,float(sys.argv[1])*1000); ok,f=c.read(); ref=th(f)
res=[]
for p in glob.glob(sys.argv[2]):
    c=cv2.VideoCapture(p); n=int(c.get(7)); best=999
    for k in range(0,n,max(1,n//6)):
        c.set(1,k); ok,f=c.read()
        if ok: best=min(best,np.abs(th(f)-ref).mean())
    res.append((best,p))
for r in sorted(res)[:5]: print(round(r[0],1),r[1])

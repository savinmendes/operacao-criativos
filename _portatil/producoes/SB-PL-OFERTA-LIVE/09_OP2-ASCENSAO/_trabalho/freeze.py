import cv2, numpy as np, sys
c=cv2.VideoCapture(sys.argv[1]); fps=c.get(5); p=None; i=0; out=[]
while True:
    ok,f=c.read()
    if not ok: break
    g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(108,192))[:130].astype(float)
    if p is not None: out.append((i/fps,np.abs(g-p).mean()))
    p=g;i+=1
a=float(sys.argv[2]); b=float(sys.argv[3])
print(" ".join(f"{t:.2f}:{d:.1f}" for t,d in out if a<=t<=b))

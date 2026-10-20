import cv2,numpy as np
c=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\_ref\48 AD.mp4")
fps=c.get(5); prev=None; i=0
while True:
    ok,f=c.read()
    if not ok: break
    t=i/fps
    if 55<=t<=90:
        g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(72,128)).astype(float)
        if prev is not None:
            d=np.abs(g-prev).mean()
            if d>12: print(round(t,2),round(d,1))
        prev=g
    i+=1

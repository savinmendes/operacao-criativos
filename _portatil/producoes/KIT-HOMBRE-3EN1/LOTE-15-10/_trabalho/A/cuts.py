import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]);fps=cap.get(5);prev=None;i=0
while True:
    ok,f=cap.read()
    if not ok:break
    g=cv2.cvtColor(cv2.resize(f,(90,160)),cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None:
        d=np.abs(g-prev).mean()
        if d>18: print(round(i/fps,3),round(d,1))
    prev=g;i+=1

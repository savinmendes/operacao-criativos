import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]);prev=None;i=0;out=[]
while True:
    ok,f=cap.read()
    if not ok:break
    g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(108,192))[:120].astype(float)
    if prev is not None: out.append((i,np.abs(g-prev).mean()))
    prev=g;i+=1
for i,d in out:
    if d>6: print(i, round(i/30,2), round(d,1))

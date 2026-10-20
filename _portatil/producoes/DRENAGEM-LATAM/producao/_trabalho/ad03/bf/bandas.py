import cv2, numpy as np, sys
cap=cv2.VideoCapture(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2].split(',')); n=0
while True:
    ok,f=cap.read()
    if not ok: break
    if n%int(sys.argv[3] if len(sys.argv)>3 else 10)==0:
        hsv=cv2.cvtColor(f[y0:y1,x0:x1],cv2.COLOR_BGR2HSV); m=cv2.inRange(hsv,(35,30,15),(95,255,140))
        m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8)); k,lab,st,_=cv2.connectedComponentsWithStats(m)
        comps=sorted([tuple(st[i]) for i in range(1,k)],key=lambda s:-s[4])[:3]
        print(n,[(s[0]+x0,s[1]+y0,s[2],s[3],s[4]) for s in comps])
    n+=1

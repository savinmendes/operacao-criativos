import cv2,numpy as np,sys
a=cv2.VideoCapture(sys.argv[1]); b=cv2.VideoCapture(sys.argv[2]); i=0
while True:
    r1,f1=a.read(); r2,f2=b.read()
    if not(r1 and r2): break
    d=np.abs(f1[:1000].astype(int)-f2[:1000].astype(int)).mean()
    if i%3==0 or d>5: print(i, round(i/30,2), round(d,1))
    i+=1

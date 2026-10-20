import cv2,numpy as np
c=cv2.VideoCapture('../../../UNICOS_HD/05.mp4'); acc=np.zeros((1280,720)); n=0
for i in range(0,2368,8):
    c.set(1,i); ok,f=c.read()
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    yel=(h>=20)&(h<=38)&(s>=110)&(v>=170)
    dark=cv2.dilate((v<70).astype(np.uint8),np.ones((5,5)))>0
    acc+=yel&dark; n+=1
r=acc.sum(1)
for y in range(850,1150,10): print(y,int(r[y:y+10].sum()))
cols=acc[900:1150].sum(0); xs=np.nonzero(cols>cols.max()*0.02)[0]; print('x',xs.min(),xs.max())

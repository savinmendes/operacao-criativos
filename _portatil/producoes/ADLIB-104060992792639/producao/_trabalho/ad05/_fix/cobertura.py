import cv2,numpy as np
BM=np.load('_tmp/boxmasks.npy',mmap_mode='r');Y0,Y1=960,1090
c=cv2.VideoCapture('../../../UNICOS_HD/05.mp4');bad=[]
for i in range(2368):
    ok,f=c.read();roi=f[Y0:Y1]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    yel=((h>=15)&(h<=42)&(s>=80)&(v>=140)).astype(np.uint8)&cv2.dilate((v<90).astype(np.uint8),np.ones((7,7),np.uint8))
    m=cv2.dilate(np.array(BM[i]),np.ones((5,5),np.uint8))
    out=int((yel&(1-m)).sum()); 
    if out>15: bad.append((i,out,int(yel.sum())))
print(len(bad));print(bad[:80])
# also full-frame: yellow text outside band?

import sys,cv2,numpy as np
src,a,b,st,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
c=cv2.VideoCapture(src);ims=[]
for i in range(a,b,st):
    c.set(1,i);ok,f=c.read()
    if not ok:break
    f=cv2.resize(f,(240,427));cv2.putText(f,f"{i} {i/24:.2f}",(5,25),0,0.7,(0,0,255),2);ims.append(f)
while len(ims)%8:ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out,np.vstack([np.hstack(ims[k:k+8]) for k in range(0,len(ims),8)]))

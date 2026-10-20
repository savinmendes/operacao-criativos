import cv2,numpy as np,sys
cap=cv2.VideoCapture("../../SB-EN-ADS-24.mp4")
frames={}
want=set()
for a,b in [(30.6,31.0),(34.6,34.95),(44.8,45.3),(46.9,47.1),(53.7,54.1),(74.7,75.0),(76.8,77.05),(80.2,80.4),(98.7,99.05),(103.3,103.5)]:
    want|=set(range(int(a*30),int(b*30)+1))
i=0;ims=[]
while True:
    ok,f=cap.read()
    if not ok: break
    if i in want:
        s=cv2.resize(f,(216,384)); cv2.putText(s,f"{i/30:.2f}",(5,25),0,0.7,(0,255,255),2); ims.append(s)
    i+=1
c=12
while len(ims)%c: ims.append(np.zeros_like(ims[0]))
cv2.imwrite("flashes.jpg",np.vstack([np.hstack(ims[k:k+c]) for k in range(0,len(ims),c)]))
print(i,len(ims))

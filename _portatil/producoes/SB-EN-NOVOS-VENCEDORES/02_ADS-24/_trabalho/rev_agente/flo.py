import cv2,numpy as np
cap=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\1-VIDEOS\ad 24.mp4"); fps=cap.get(5)
want=set()
for a,b in [(50.5,51.05),(52.95,53.25),(123.9,124.2),(38.3,38.7),(88.7,88.9),(93.75,93.95)]:
    want|=set(range(int(a*fps),int(b*fps)+1))
i=0;ims=[]
while True:
    ok,f=cap.read()
    if not ok: break
    if i in want:
        s=cv2.resize(f,(216,384)); cv2.putText(s,f"{i/fps:.2f}",(5,25),0,0.7,(0,255,255),2); ims.append(s)
    i+=1
c=12
while len(ims)%c: ims.append(np.zeros_like(ims[0]))
cv2.imwrite("flashes_orig.jpg",np.vstack([np.hstack(ims[k:k+c]) for k in range(0,len(ims),c)])); print(fps,len(ims))

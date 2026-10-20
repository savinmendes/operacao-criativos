import cv2,numpy as np,json
cap=cv2.VideoCapture(r"../../original_wsen5drS7Nk.mp4");prev=None;i=0;C=[]
while True:
    ok,f=cap.read()
    if not ok:break
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None:
        d=float(np.abs(g-prev).mean())
        if d>12:C.append([i,round(i/30,2),round(d,1)])
    prev=g;i+=1
print(i);print(C);json.dump(C,open("cortes.json","w"))

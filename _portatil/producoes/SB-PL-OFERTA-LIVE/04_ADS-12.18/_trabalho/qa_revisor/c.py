import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
cap=cv2.VideoCapture(V)
ts=[0.5,2.0,2.5,3.0,4.5,7.0,8.0,9.0,11.0,13.0,14.0,16.5,17.0,18.0,19.0,19.5,20.5,21.5,22.0,24.0,27.0,27.5,28.5,29.0,30.0,31.0,32.0]
rows=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(t*30)); ok,f=cap.read()
    c=f[700:1130].copy(); cv2.putText(c,f"{t}",(5,30),0,1,(0,255,255),2); rows.append(cv2.resize(c,(360,215)))
while len(rows)%3: rows.append(np.zeros_like(rows[0]))
g=np.vstack([np.hstack(rows[i:i+3]) for i in range(0,len(rows),3)])
cv2.imwrite("legendas.jpg",g)

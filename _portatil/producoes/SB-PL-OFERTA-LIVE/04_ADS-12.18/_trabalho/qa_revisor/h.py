import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
cap=cv2.VideoCapture(V)
ks=[814,815,816,854,855,856,894,895,896,950,953,956,958,961,964]
out=[]
for k in ks:
    cap.set(1,k); f=cap.read()[1]; c=cv2.resize(f[180:480,270:530],(260,300)); cv2.putText(c,f"{k} {k/30:.2f}",(3,18),0,0.55,(0,255,255),2); out.append(c)
cv2.imwrite("dentes.jpg",np.vstack([np.hstack(out[i:i+5]) for i in range(0,15,5)]))

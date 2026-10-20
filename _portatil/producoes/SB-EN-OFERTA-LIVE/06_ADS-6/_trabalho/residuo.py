import cv2, numpy as np
from mascara2 import mascara
cap=cv2.VideoCapture("base_limpa.mp4"); i=0; hits=[]
while True:
    ok,f=cap.read()
    if not ok: break
    if i%2==0:
        # resíduo: branco puro / amarelo saturado na faixa
        roi=f[1300:1720]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        yel=((hsv[...,0]>=18)&(hsv[...,0]<=40)&(hsv[...,1]>110)&(hsv[...,2]>140)).sum()
        m=mascara(f).sum()
        if yel>150 or m>0: hits.append((i,int(yel),int(m)))
    i+=1
print(len(hits)); print(hits[:300])

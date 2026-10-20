import cv2, numpy as np, sys
C=r"C:\Users\PICHAU\Downloads\1-VIDEOS\SB-CORPO_CTA_COMPLETO_JESU.mp4"
cap=cv2.VideoCapture(C); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(90,160)).astype(float))
fr=np.array(fr)
for n in ["corpo","clipA","clipB"]:
    c=cv2.VideoCapture(rf"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\piloto\_trabalho\heygen_in\{n}_src.mp4")
    res=[]
    for k in range(3):
        ok,f=c.read(); g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(90,160)).astype(float)
        d=np.abs(fr[:,:100]-g[:100]).mean(axis=(1,2)); i=int(d.argmin()); res.append((i,i/25,round(d[i],2)))
    print(n,res)

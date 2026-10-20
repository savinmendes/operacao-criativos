import cv2, numpy as np, subprocess
src=r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"
cap=cv2.VideoCapture(src); N=int(cap.get(7)); fr=[]
for t in np.linspace(5,N-10,40).astype(int):
    cap.set(1,t); ok,f=cap.read(); fr.append(f[250:780].astype(np.float32))
A=np.stack(fr); sd=A.std(0).mean(-1); med=np.median(A,0)
static=(sd<6).astype(np.uint8)
cv2.imwrite("card_med.png",med.astype(np.uint8)); cv2.imwrite("card_static.png",static*255)
ys,xs=np.where(static>0); print("bbox",xs.min(),ys.min()+250,xs.max(),ys.max()+250)
# perfil por linha
for y in range(0,530,10): 
    r=np.where(static[y]>0)[0]; print(y+250, (r.min(),r.max()) if len(r) else None)

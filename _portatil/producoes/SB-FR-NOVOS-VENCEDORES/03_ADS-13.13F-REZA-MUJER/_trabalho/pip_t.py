import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
SRC=r"C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4"; BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
A=list(quadros(SRC,0,176)); B=list(quadros(BASE,0,180))
M=np.float32([[0.6093,0,281.03],[0,0.6093,680.26]])
Wb=[cv2.warpAffine(b,M,(720,1280),flags=cv2.INTER_AREA) for b in B]
out=[]
for n in range(0,176,1):
    r=[]
    for d in range(-3,4):
        m=n+d
        if 0<=m<180: r.append((np.abs(A[n][720:1050,400:660].astype(int)-Wb[m][720:1050,400:660]).mean(),d))
    out.append((n,)+min(r))
for o in out[::5]: print(o[0],round(o[1],2),o[2])

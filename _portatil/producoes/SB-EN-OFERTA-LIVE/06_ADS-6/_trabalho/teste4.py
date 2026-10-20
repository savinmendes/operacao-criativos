import cv2,numpy as np
from teste_lama2 import limpar
from mascara2 import mascara
s=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"); rows=[]
K=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,41))
for i in [2060,2096,2106,2116,2126,2136,2146]:
    s.set(1,i); _,f=s.read(); m=cv2.dilate(mascara(f),K)
    ys=np.where(m.any(1))[0]; mb=np.zeros_like(m); mb[ys.min():ys.max()+1,:]=1
    a=limpar(f,m,0.5); b=limpar(f,mb,0.5)
    rows.append(np.hstack([cv2.resize(a[1300:1720],(540,210)),cv2.resize(b[1300:1720],(540,210))]))
cv2.imwrite("diag5.jpg",np.vstack(rows))

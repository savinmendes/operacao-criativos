import cv2,numpy as np
from teste_lama2 import limpar
from mascara2 import mascara
s=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"); rows=[]
for t in [7.6,107.2,119.5,130.4,32.5,131.5,77.4]:
    fi=int(t/1.0087*30); s.set(1,fi); _,f=s.read(); m=mascara(f)
    m2=cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,41)))
    rows.append(np.hstack([cv2.resize(limpar(f,m2,0.5)[1330:1700],(540,185)),cv2.resize(f[1330:1700],(540,185))]))
cv2.imwrite("diag4.jpg",np.vstack(rows))

import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
SRC=r"C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4"; BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
n=100; a=list(quadros(SRC,n,1))[0]; b=list(quadros(BASE,n,1))[0]
s=0.6; tx=392-180*s; ty=774-150*s
M=np.float32([[s,0,tx],[0,s,ty]]); w=cv2.warpAffine(b,M,(720,1280))
cr=lambda x: x[640:1280,260:720]
cv2.imwrite("q/viz.jpg",np.hstack([cr(a),cr(w),cv2.absdiff(cr(a),cr(w))*3]))

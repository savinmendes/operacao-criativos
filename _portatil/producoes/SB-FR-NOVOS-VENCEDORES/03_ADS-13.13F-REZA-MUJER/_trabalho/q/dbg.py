import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
n=52
s=list(quadros("src13.mp4",n,1))[0]; h=list(quadros("heygen/A_heygen.mp4",n,1))[0]
b=list(quadros(r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4",n,1))[0]
MW=np.float32([[0.6093,0,281.03],[0,0.6093,680.26]])
cr=lambda f: cv2.resize(f[760:1000,400:680],None,fx=2,fy=2)
cv2.imwrite("q/dbg.jpg",np.hstack([cr(s),cr(cv2.warpAffine(h,MW,(720,1280))),cr(cv2.warpAffine(b,MW,(720,1280)))]))

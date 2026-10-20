import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
SRC=r"C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4"; BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
A=list(quadros(SRC,0,180)); B=list(quadros(BASE,0,200))
def sc(n,m,s):
    tpl0=B[m][150:600,180:600]; t=cv2.resize(tpl0,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
    g=lambda x: cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
    r=cv2.matchTemplate(g(A[n]),g(t),cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(r); return mv,ml
for n in [30,100]:
    res=[(round(sc(n,m,0.6)[0],3),m) for m in range(max(0,n-30),n+30,3)]
    print(n,sorted(res)[-4:])
for s in [0.58,0.6,0.62,0.64,0.66,0.68,0.70]: print(s,sc(100,100,s))

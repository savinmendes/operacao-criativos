import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
SRC=r"C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4"; BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
for n in [20,90,150]:
    a=list(quadros(SRC,n,1))[0]; b=list(quadros(BASE,n,1))[0]
    tpl0=b[150:600,180:600]  # rosto+barba
    best=None
    for s in np.arange(0.55,0.80,0.005):
        t=cv2.resize(tpl0,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
        r=cv2.matchTemplate(a,t,cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(r)
        if best is None or mv>best[0]: best=(mv,s,ml)
    mv,s,ml=best; tx=ml[0]-180*s; ty=ml[1]-150*s
    print(n,round(mv,4),round(s,4),round(tx,2),round(ty,2))

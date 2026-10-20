import cv2, numpy as np
Y0,Y1=1300,1720
def mascara(f):
    roi=f[Y0:Y1]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    bh=cv2.morphologyEx(v,cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
    e=(bh>55).astype(np.float32)
    yel=((h>=18)&(h<=40)&(s>110)&(v>140)).astype(np.float32)
    wht=((v>225)&(s<40)).astype(np.float32)
    # densidade de contorno e de "tinta" (branco/amarelo) em janela
    de=cv2.blur(e,(41,41)); dt=cv2.blur(np.maximum(yel,wht),(41,41)); dy=cv2.blur(yel,(41,41))
    core=(((de>0.10)&(dt>0.15))|(dy>0.10)).astype(np.uint8)
    core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,np.ones((21,41),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(core)
    keep=np.zeros_like(core)
    for k in range(1,n):
        if st[k,4]>=2500 and st[k,3]>=50: keep[lab==k]=1
    m=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)))
    full=np.zeros(f.shape[:2],np.uint8); full[Y0:Y1]=m; return full
if __name__=="__main__":
    cap=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4")
    outs=[]
    for t in [30,60,10,66,69,102,2,120]:
        cap.set(0,t*1000); ok,f=cap.read(); m=mascara(f)
        o=f.copy(); o[m>0]=(0.5*o[m>0]+[0,0,127]).astype(np.uint8); outs.append(cv2.resize(o[1280:1740],(540,230)))
    cv2.imwrite("mask_teste.jpg",np.vstack([np.hstack(outs[:4]),np.hstack(outs[4:])]))

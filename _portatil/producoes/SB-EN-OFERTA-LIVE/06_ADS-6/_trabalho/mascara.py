import cv2, numpy as np
Y0,Y1=1300,1720
def mascara(f):
    roi=f[Y0:Y1]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2].astype(np.float32)
    bg=cv2.blur(v,(41,41))
    edge=((bg-v)>45).astype(np.uint8)
    near=cv2.dilate(edge,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
    yel=((h>=18)&(h<=40)&(s>110)&(v>140)).astype(np.uint8)
    wht=((v>215)&(s<45)).astype(np.uint8)&near
    txt=yel|wht
    txt=cv2.morphologyEx(txt,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    blob=cv2.morphologyEx(txt|(edge&cv2.dilate(txt,np.ones((15,15),np.uint8))),cv2.MORPH_CLOSE,np.ones((31,45),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(blob)
    keep=np.zeros_like(blob)
    for k in range(1,n):
        if st[k,4]>=1500 and st[k,3]>=45: keep[lab==k]=1
    cs,_=cv2.findContours(keep,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(keep,cs,-1,1,-1)
    m=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(21,21)))
    full=np.zeros(f.shape[:2],np.uint8); full[Y0:Y1]=m; return full
if __name__=="__main__":
    cap=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4")
    outs=[]
    for t in [60,10,36.5,45,100,130]:
        cap.set(0,t*1000); ok,f=cap.read(); m=mascara(f)
        o=f.copy(); o[m>0]=(0.5*o[m>0]+[0,0,127]).astype(np.uint8); outs.append(cv2.resize(o[1250:1750],(540,250)))
    cv2.imwrite("mask_teste.jpg",np.vstack(outs))

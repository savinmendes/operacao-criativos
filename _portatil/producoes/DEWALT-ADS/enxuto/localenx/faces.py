import cv2,numpy as np
cc=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
c=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\_ref\48 AD.mp4")
for a,b in [(62.8,69.6),(81.0,85.6)]:
    bx=[]
    for t in np.arange(a,b,0.3):
        c.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=c.read()
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
        fs=cc.detectMultiScale(g,1.1,5,minSize=(80,80))
        if len(fs): x,y,w,h=max(fs,key=lambda r:r[2]); bx.append((x,y,x+w,y+h)); 
        else: print(" no face",round(t,1))
    bx=np.array(bx); print(a,b,"min",bx.min(0),"max",bx.max(0))

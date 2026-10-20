import cv2,numpy as np,json
cap=cv2.VideoCapture('../../SB-EN-ADS-24.mp4')
cas=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
ch=json.load(open('../chunks.json'))
w=[(d['s']+0.05,d['e']+0.05) for d in json.load(open('../audio/velho_stt.json',encoding='utf-8'))]+[(d['s']+5.75,d['e']+5.75) for d in json.load(open('../audio/anjo_stt.json',encoding='utf-8'))]
def fala(t): return any(a-0.03<=t<=b+0.03 for a,b in w)
step=5  # 6 fps
frames=[];i=0;last=None;faces={}
while True:
    ok,f=cap.read()
    if not ok: break
    t=i/30
    inch=[c for c in ch if c[1]<=t<c[2]]
    if inch and i%step==0:
        g=cv2.cvtColor(f[0:700],cv2.COLOR_BGR2GRAY)
        d=cas.detectMultiScale(g,1.1,5,minSize=(50,50))
        if len(d): last=max(d,key=lambda r:r[2]); 
        if last is not None:
            x,y,ww,hh=last; x0=x+int(ww*0.15); x1=x+int(ww*0.85); y0=y+int(hh*0.55); y1=min(y+int(hh*1.1),1280)
            crop=cv2.resize(f[y0:y1,x0:x1],(140,110))
        else: crop=np.zeros((110,140,3),np.uint8)
        col=(0,200,0) if fala(t) else (0,0,255)
        crop=cv2.copyMakeBorder(crop,4,4,4,4,cv2.BORDER_CONSTANT,value=col)
        cv2.putText(crop,f"{t:.1f}{inch[0][0]}",(4,14),0,0.42,(0,255,255),1)
        frames.append(crop)
    i+=1
c=16;per=16*14
for s in range(0,len(frames),per):
    ims=frames[s:s+per]
    while len(ims)%c: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f'boca_{s//per}.jpg',np.vstack([np.hstack(ims[k:k+c]) for k in range(0,len(ims),c)]))
print(len(frames))

import cv2,numpy as np,json,sys
box={'V':(322,189,152,180),'A1':(394,214,113,130),'A21':(357,99,131,154),'A22a':(348,224,100,118),'A22b':(346,224,102,118),'C':(297,162,192,226)}
dflt=(352,229,100,118)
w=[(d['s']+0.05,d['e']+0.05,d['w']) for d in json.load(open('../audio/velho_stt.json',encoding='utf-8'))]+[(d['s']+5.75,d['e']+5.75,d['w']) for d in json.load(open('../audio/anjo_stt.json',encoding='utf-8'))]
def fala(t):
    for a,b,x in w:
        if a-0.03<=t<=b+0.03: return x
    return None
ch=json.load(open('../chunks.json'))
sel=sys.argv[1].split(',')
for n,a,b in ch:
    if n not in sel: continue
    x,y,bw,bh=box.get(n,dflt)
    cap=cv2.VideoCapture('../../SB-EN-ADS-24.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,int(round(a*30)))
    ims=[];i=int(round(a*30))
    while i<int(round(b*30)):
        ok,f=cap.read(); 
        if not ok: break
        t=i/30
        if i%3==0:
            cr=f[y+int(bh*0.45):y+int(bh*1.05), x+int(bw*0.1):x+int(bw*0.9)]
            cr=cv2.resize(cr,(150,int(150*cr.shape[0]/cr.shape[1])))
            wd=fala(t); col=(0,190,0) if wd else (0,0,255)
            cr=cv2.copyMakeBorder(cr,18,3,3,3,cv2.BORDER_CONSTANT,value=col)
            cv2.putText(cr,f"{t:.2f} {wd or '-'}"[:22],(3,13),0,0.4,(255,255,255),1)
            ims.append(cr)
        i+=1
    c=12
    while len(ims)%c: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f'boca_{n}.jpg',np.vstack([np.hstack(ims[k:k+c]) for k in range(0,len(ims),c)]))

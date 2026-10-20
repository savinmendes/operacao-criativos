# uso: python folha.py nome x,y,w,h passo [q0 q1]  -> out/folha_<nome>.jpg (cima: final, baixo: original; barra verde = voz ES)
import sys, cv2, numpy as np, librosa, json
from pathlib import Path
n=sys.argv[1]; x,y,w,h=map(int,sys.argv[2].split(',')); passo=int(sys.argv[3])
FPS=json.load(open('segs.json'))["fps"]
def ler(p):
    c=cv2.VideoCapture(p); r=[]
    while True:
        ok,f=c.read()
        if not ok: break
        r.append(f[y:y+h,x:x+w])
    return r
A=ler(f'out/full_{n}.mp4'); B=ler(f'in/orig_{n}.mp4')
q0,q1=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (0,len(A))
yv,sr=librosa.load(f'in/es_{n}.mp3',sr=16000); e=librosa.feature.rms(y=yv,frame_length=int(sr/FPS),hop_length=int(sr/FPS))[0]
db=20*np.log10(e+1e-9); fala=db>db.max()-30
cols=[]
for k in range(q0,min(q1,len(A),len(B)),passo):
    a=cv2.resize(A[k],(120,int(120*h/w))); b=cv2.resize(B[k],(120,int(120*h/w)))
    bar=np.zeros((12,120,3),np.uint8); bar[:]=(0,200,0) if (k<len(fala) and fala[k]) else (60,60,60)
    cv2.putText(bar,f"{k}",(2,10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(255,255,255),1)
    cols.append(np.vstack([bar,a,b]))
rows=[np.hstack(cols[i:i+12]+[np.zeros_like(cols[0])]*(12-len(cols[i:i+12]))) for i in range(0,len(cols),12)]
cv2.imwrite(f'out/folha_{n}.jpg',np.vstack(rows)); print(len(cols))

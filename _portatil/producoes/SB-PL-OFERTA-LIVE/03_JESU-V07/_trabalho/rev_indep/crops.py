import cv2, numpy as np, mediapipe as mp
V=r'..\..\SB-PL-JESU-V07.mp4'
cap=cv2.VideoCapture(V); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(f)
print(len(fr))
# legenda: a cada 0.5s, montagem
tiles=[]
for i,t in enumerate(np.arange(0.25,30.6,0.5)):
    f=fr[min(int(t*30),len(fr)-1)][1365:1565].copy()
    cv2.putText(f,f'{t:.2f}',(5,30),0,1,(0,0,255),2)
    tiles.append(cv2.resize(f,(540,100)))
for k in range(0,len(tiles),16):
    g=tiles[k:k+16]
    while len(g)%2: g.append(np.zeros_like(g[0]))
    rows=[np.hstack(g[j:j+2]) for j in range(0,len(g),2)]
    cv2.imwrite(f'leg_{k//16}.jpg',np.vstack(rows))
# full frame sheet
th=[cv2.resize(fr[int(t*30)],(216,384)) for t in np.arange(0.2,30.6,1.0)]
while len(th)%8: th.append(np.zeros_like(th[0]))
cv2.imwrite('sheet.jpg',np.vstack([np.hstack(th[j:j+8]) for j in range(0,len(th),8)]))
# boca
fm=mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=2)
times=[0.5,1.85,1.95,2.5,4.3,4.55,4.75,4.9,6.5,8.65,8.8,14.2,15.5,17.65,22.45,24,26.2]
out=[]
for t in times:
    f=fr[int(t*30)]
    r=fm.process(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
    if not r.multi_face_landmarks:
        c=np.zeros((240,320,3),np.uint8); cv2.putText(c,f'{t} noface',(5,30),0,0.8,(0,0,255),2); out.append(c); continue
    lm=r.multi_face_landmarks[0].landmark
    h,w=f.shape[:2]
    x=int(np.mean([lm[i].x for i in (13,14,61,291)])*w); y=int(np.mean([lm[i].y for i in (13,14)])*h)
    gap=abs(lm[14].y-lm[13].y)*h; fw=abs(lm[234].x-lm[454].x)*w
    s=int(fw*0.45)
    c=f[max(0,y-s):y+s, max(0,x-int(s*1.33)):x+int(s*1.33)]
    c=cv2.resize(c,(320,240))
    cv2.putText(c,f'{t} gap{gap/fw:.3f}',(5,25),0,0.7,(0,0,255),2)
    out.append(c); print(t,x,y,round(gap/fw,3))
while len(out)%6: out.append(np.zeros_like(out[0]))
cv2.imwrite('boca.jpg',np.vstack([np.hstack(out[j:j+6]) for j in range(0,len(out),6)]))
# flash nos cortes: diferenca media de quadros vizinhos
d=[float(np.mean(cv2.absdiff(fr[i],fr[i-1]))) for i in range(1,len(fr))]
for i,v in enumerate(d):
    if v>25: print('corte',round((i+1)/30,3),round(v,1))

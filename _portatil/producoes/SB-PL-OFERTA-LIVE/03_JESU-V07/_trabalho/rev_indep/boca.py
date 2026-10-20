import cv2, numpy as np, sys
sys.path.insert(0,r'C:/Users/PICHAU/Downloads/Produtividade com ia/kit-edicao-criativos/ferramentas')
import checar_lipsync as cl
det=cl.Rastreador()
V=r'..\..\SB-PL-JESU-V07.mp4'
cap=cv2.VideoCapture(V); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(f)
def mouth(t):
    f=fr[int(round(t*30))]
    p=det.pontos(f)
    if p is None: print(t,'noface'); return None
    fw=np.linalg.norm(p[234]-p[454]); m=p[[13,14,61,291]].mean(0); cx,cy=int(m[0]),int(m[1]+fw*0.08)
    print(t,'gap',round(np.linalg.norm(p[13]-p[14])/fw,3))
    h=int(fw*0.42); w=int(fw*0.57)
    return cv2.resize(f[cy-h:cy+h, cx-w:cx+w],(360,264))
times=[('hook fala',1.0),('hook pausa',1.85),('hook pausa',1.95),('hook pausa',4.3),('hook pausa',4.55),
('c1 pausa',4.72),('c1 pausa',4.9),('c1 fala',6.6),('c1 pausa',8.65),('c1 pausa',8.8),
('c2 pausa',14.2),('c2 fala',15.6),('c2 pausa',17.65),('c2 fala',17.85),
('c3 pausa',22.45),('c3 fala',24.0),('c3 pausa',26.2),('c3 fala',25.3)]
out=[]
for lab,t in times:
    c=mouth(t)
    if c is None: c=np.zeros((264,360,3),np.uint8)
    c=c.copy(); cv2.putText(c,f'{lab} {t}',(5,25),0,0.7,(0,0,255),2); out.append(c)
cv2.imwrite('boca.jpg',np.vstack([np.hstack(out[j:j+6]) for j in range(0,len(out),6)]))
d=[float(np.mean(cv2.absdiff(fr[i],fr[i-1]))) for i in range(1,len(fr))]
for i,v in enumerate(d):
    if v>20: print('corte',round((i+1)/30,3),round(v,1),'prev',round(d[i-1],1),'next',round(d[i+1],1) if i+1<len(d) else '')
f=fr[int(27.25*30)]; cv2.imwrite('door2725.jpg',cv2.resize(f[1250:1450,340:740],(800,400),interpolation=cv2.INTER_NEAREST))

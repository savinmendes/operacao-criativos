# Revisor AD05: quadro inteiro, final (cima) x original no mesmo tempo (baixo), de N em N quadros (30 fps).
import sys, cv2, numpy as np
t0,t1,out=float(sys.argv[1]),float(sys.argv[2]),sys.argv[3]; passo=int(sys.argv[4]) if len(sys.argv)>4 else 3; porl=int(sys.argv[5]) if len(sys.argv)>5 else 16
W=int(sys.argv[6]) if len(sys.argv)>6 else 120
P=r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639"
cf=cv2.VideoCapture(P+r"\producao\AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"); co=cv2.VideoCapture(P+r"\UNICOS_HD\05.mp4")
H=int(W*1280/720); tiles=[]
for q in range(int(t0*30),int(t1*30)+1,passo):
    t=q/30; to=t if t*24<1286 else t+70/24
    cf.set(1,q); ok,f=cf.read(); co.set(1,int(round(to*24))); ok2,o=co.read()
    if not ok: break
    tl=np.full((2*H+16,W,3),255,np.uint8); tl[:H]=cv2.resize(f,(W,H)); tl[H:2*H]=cv2.resize(o,(W,H))
    cv2.putText(tl,f"{t:.2f}",(2,2*H+13),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,0),1); tiles.append(tl)
rows=[]
for i in range(0,len(tiles),porl):
    l=tiles[i:i+porl]; l+= [np.full_like(tiles[0],255)]*(porl-len(l)); rows.append(np.hstack(l))
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85]); print("ok",out,len(tiles))

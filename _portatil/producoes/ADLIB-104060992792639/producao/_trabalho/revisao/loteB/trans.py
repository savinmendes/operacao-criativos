# 1 em 1 quadro: final (cima) x original (baixo), quadro inteiro reduzido. Uso: python trans.py NN t0 t1 saida.jpg
import sys, cv2, numpy as np
from pathlib import Path
NN,t0,t1,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
P=Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
fin=next((P/"producao").glob(f"AD {NN} - *-ES-LATAM.mp4")); ori=P/"UNICOS_HD"/f"{NN}.mp4"
def frames(p,fps_out=30):
    c=cv2.VideoCapture(str(p)); fps=c.get(cv2.CAP_PROP_FPS); r=[]
    for q in range(int(round(t0*30)),int(round(t1*30))+1):
        c.set(cv2.CAP_PROP_POS_FRAMES,int(round(q/30*fps))); ok,f=c.read(); r.append((q,cv2.resize(f,(108,192)) if ok else np.zeros((192,108,3),np.uint8)))
    return r
A=frames(fin); B=frames(ori); tiles=[]
for (q,a),(_,b) in zip(A,B):
    t=np.full((192*2+18,108,3),255,np.uint8); t[:192]=a; t[192:384]=b
    cv2.putText(t,f"{q/30:.2f}",(2,398),cv2.FONT_HERSHEY_SIMPLEX,0.38,(0,0,0),1); tiles.append(t)
rows=[np.hstack(tiles[i:i+12]+[np.full_like(tiles[0],255)]*(12-len(tiles[i:i+12]))) for i in range(0,len(tiles),12)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85]); print(out)

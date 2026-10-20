import cv2, json, numpy as np, sys
from comum3 import quadros
SEG=json.load(open("heygen_in/seg.json")); ts=[float(x) for x in sys.argv[2].split(",")]; out=sys.argv[3]
fr={int(round(t*30)):None for t in ts}
for i,f in enumerate(quadros(sys.argv[1],w=1080,h=1920)):
    if i in fr: fr[i]=f
    if i>max(fr): break
cells=[]
for t in ts:
    f=fr[int(round(t*30))]
    c=f[350:1250,190:890].copy(); c=cv2.resize(c,(280,360)); cv2.putText(c,f"{t:.2f}",(5,25),0,0.8,(0,255,255),2); cells.append(c)
rows=[cv2.hconcat(cells[i:i+8]+[np.zeros_like(cells[0])]*(8-len(cells[i:i+8]))) for i in range(0,len(cells),8)]
cv2.imwrite(out,cv2.vconcat(rows))

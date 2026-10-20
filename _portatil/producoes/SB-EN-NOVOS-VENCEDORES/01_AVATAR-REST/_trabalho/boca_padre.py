import cv2,numpy as np,json,sys
from comum3 import quadros
a,b=float(sys.argv[1]),float(sys.argv[2]); out=sys.argv[3]
W=json.load(open("palavras_en.json",encoding="utf-8"))
cells=[]
for i,f in enumerate(quadros(sys.argv[4] if len(sys.argv)>4 else "SB-EN-AVATAR-REST_v1.mp4",w=1080,h=1920)):
    t=i/30
    if t>b: break
    if t>=a and i%2==0:
        c=cv2.resize(f[560:900,340:740],(160,136)); w=next((x[0] for x in W if x[1]<=t<x[2]),"-")
        cv2.putText(c,f"{t:.2f} {w}",(2,14),0,0.42,(0,255,255),1); cells.append(c)
while len(cells)%12: cells.append(np.zeros_like(cells[0]))
cv2.imwrite(out,cv2.vconcat([cv2.hconcat(cells[i:i+12]) for i in range(0,len(cells),12)]))

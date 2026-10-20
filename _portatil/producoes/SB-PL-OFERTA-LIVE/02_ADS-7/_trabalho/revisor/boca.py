import cv2,sys,numpy as np
v=sys.argv[1]; out=sys.argv[2]; ts=[float(x) for x in sys.argv[3].split(',')]
cap=cv2.VideoCapture(v); tiles=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES,round(t*30)); ok,f=cap.read()
    c=f[495:945,360:735].copy(); cv2.putText(c,f"{t:.3f}",(5,35),0,1.1,(0,255,255),3); tiles.append(cv2.resize(c,(250,300)))
while len(tiles)%6: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+6]) for i in range(0,len(tiles),6)]
cv2.imwrite(out,np.vstack(rows))

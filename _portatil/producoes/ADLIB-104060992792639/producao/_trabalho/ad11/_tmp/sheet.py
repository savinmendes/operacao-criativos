import cv2, sys, numpy as np
src, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
ts=[float(x) for x in sys.argv[4:]]
cap=cv2.VideoCapture(src); tiles=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t*1000); ok,f=cap.read()
    f=cv2.resize(f,(w,int(w*f.shape[0]/f.shape[1])))
    cv2.putText(f,f"{t}",(4,22),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2); tiles.append(f)
cols=min(len(tiles),6)
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]
cv2.imwrite(out,np.vstack(rows))

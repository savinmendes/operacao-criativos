import cv2,numpy as np,sys
from comum3 import quadros
ts=[float(x) for x in sys.argv[2].split(",")]; fr={int(round(t*30)):t for t in ts}; cells=[]
for i,f in enumerate(quadros(sys.argv[1],w=1080,h=1920)):
    if i in fr:
        c=cv2.resize(f,(270,480)); cv2.putText(c,f'{fr[i]:.2f}',(4,24),0,0.8,(0,255,255),2); cells.append(c)
    if i>max(fr): break
n=int(sys.argv[4]) if len(sys.argv)>4 else 8
while len(cells)%n: cells.append(np.zeros_like(cells[0]))
cv2.imwrite(sys.argv[3],cv2.vconcat([cv2.hconcat(cells[i:i+n]) for i in range(0,len(cells),n)]))

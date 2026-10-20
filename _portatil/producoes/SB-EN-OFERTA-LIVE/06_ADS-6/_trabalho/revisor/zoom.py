import cv2, numpy as np, sys
V=r'C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\06_ADS-6\SB-EN-ADS-6.mp4'
cap=cv2.VideoCapture(V)
ts=[float(x) for x in sys.argv[2].split(',')]
y0,y1,x0,x1=[int(v) for v in sys.argv[3].split(',')]
tiles=[]
for t in ts:
    cap.set(1,round(t*30)); ok,f=cap.read(); s=f[y0:y1,x0:x1].copy()
    cv2.putText(s,f'{t:.2f}',(5,30),0,1,(0,0,255),2); tiles.append(s)
cols=int(sys.argv[4]) if len(sys.argv)>4 else 2
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
img=np.vstack([np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)])
cv2.imwrite(sys.argv[1],img)

import cv2, numpy as np
V=r'C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\06_ADS-6\SB-EN-ADS-6.mp4'
cap=cv2.VideoCapture(V); tiles=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    if i%15==7:
        s=cv2.resize(f[1400:1600],(540,100)); cv2.putText(s,f'{i/30:.1f}',(3,18),0,0.55,(0,0,255),2); tiles.append(s)
    i+=1
per=60
for k in range(0,len(tiles),per):
    ch=tiles[k:k+per]
    while len(ch)<per: ch.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f'f2_{k//per}.jpg',np.vstack([np.hstack(ch[j:j+3]) for j in range(0,per,3)]),[cv2.IMWRITE_JPEG_QUALITY,88])
print(len(tiles))

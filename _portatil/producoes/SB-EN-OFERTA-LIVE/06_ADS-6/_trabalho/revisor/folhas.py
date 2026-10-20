import cv2, numpy as np, sys
V=r'C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\06_ADS-6\SB-EN-ADS-6.mp4'
cap=cv2.VideoCapture(V); fps=30; N=int(cap.get(7))
tiles=[]
for t in np.arange(0.5,138.1,1.0):
    cap.set(1,int(t*fps)); ok,f=cap.read()
    if not ok: continue
    s=f[1300:1720].copy(); s=cv2.resize(s,(540,210))
    cv2.putText(s,f'{t:.1f}',(5,25),0,0.8,(0,0,255),2); tiles.append(s)
per=24
for i in range(0,len(tiles),per):
    ch=tiles[i:i+per]
    while len(ch)<per: ch.append(np.zeros_like(tiles[0]))
    rows=[np.hstack(ch[j:j+2]) for j in range(0,per,2)]
    cv2.imwrite(f'faixa_{i//per}.jpg',np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
print(len(tiles))

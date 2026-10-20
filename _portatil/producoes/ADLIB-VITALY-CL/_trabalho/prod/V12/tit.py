import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4"
cap=cv2.VideoCapture(V); i=0; prevt=None
while True:
    r,f=cap.read()
    if not r: break
    t=f[20:180]; m=(t.min(2)>235)
    ts=cv2.resize((m*255).astype(np.uint8),(72,16)).astype(int)
    if prevt is not None and np.abs(ts-prevt).mean()>12:
        rows=np.where(m.sum(1)>300)[0]; cols=np.where(m.sum(0)>15)[0]
        print(i,f"{i/30:.3f}", (rows[0]+20,rows[-1]+20,cols[0],cols[-1]) if len(rows) else None)
    prevt=ts; i+=1

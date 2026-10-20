import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
cap=cv2.VideoCapture(V); prev=None; i=0; d=[]; lum=[]
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(cv2.resize(f,(180,320)),cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum.append(g.mean())
    d.append(0 if prev is None else np.abs(g-prev).mean()); prev=g; i+=1
d=np.array(d); print("frames",i)
for k in range(1,len(d)):
    if d[k]>12: print(f"cut f{k} t={k/30:.3f} diff={d[k]:.1f} lum {lum[k-1]:.0f}->{lum[k]:.0f}")
# flash: frame differs from both neighbors while neighbors similar
for k in range(1,len(d)-1):
    pass

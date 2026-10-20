import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
cap=cv2.VideoCapture(V); F=[]
while True:
    ok,f=cap.read()
    if not ok: break
    F.append(f)
def lab(c,k): cv2.putText(c,f"{k} {k/30:.2f}",(3,18),0,0.55,(0,255,255),2); return c
# jump cuts
rows=[]
for c in [846,911,950]:
    rows.append(np.hstack([lab(cv2.resize(F[k][130:530,250:550],(180,240)),k) for k in range(c-3,c+3)]))
cv2.imwrite("jumps.jpg",np.vstack(rows))
# CTA mouth every 4 frames
ks=list(range(799,994,4)); cr=[lab(cv2.resize(F[k][300:460,300:500],(150,120)),k) for k in ks]
while len(cr)%8: cr.append(np.zeros_like(cr[0]))
cv2.imwrite("cta_boca.jpg",np.vstack([np.hstack(cr[i:i+8]) for i in range(0,len(cr),8)]))
# hook face zoom
ks=list(range(0,168,6)); cr=[lab(cv2.resize(F[k][560:880,400:680],(210,240)),k) for k in ks]
while len(cr)%7: cr.append(np.zeros_like(cr[0]))
cv2.imwrite("hook_boca.jpg",np.vstack([np.hstack(cr[i:i+7]) for i in range(0,len(cr),7)]))
# mid-frame motion within CTA: per-frame diff of face region to spot back-and-forth
g=[cv2.cvtColor(F[k][130:530,250:550],cv2.COLOR_BGR2GRAY).astype(float) for k in range(799,994)]
ref=g[0]
import sys

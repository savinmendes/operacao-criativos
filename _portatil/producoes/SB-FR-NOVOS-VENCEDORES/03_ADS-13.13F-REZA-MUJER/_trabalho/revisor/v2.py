import numpy as np,cv2
from fr import frames
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
def grid(ims,cols):
    h,w=ims[0].shape[:2];rows=(len(ims)+cols-1)//cols
    g=np.zeros((rows*h,cols*w,3),np.uint8)
    for k,im in enumerate(ims): g[(k//cols)*h:(k//cols+1)*h,(k%cols)*w:(k%cols+1)*w]=im
    return g
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'
P=[]
for i,f in enumerate(frames(V)):
    if i>=170: break
    P.append(f[640:1280].copy())
P=np.stack(P)
z=lambda f,s=3: cv2.resize(f[830-640:940-640,480:620],None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC)
cv2.imwrite('v2_dedo_boca_1.3-2.1.jpg',grid([lab(z(P[i]),f'{i/30:.2f}') for i in range(39,63)],6),[cv2.IMWRITE_JPEG_QUALITY,92])
cv2.imwrite('v2_boca_zoom.jpg',grid([lab(z(P[i]),f'{i/30:.2f}') for i in [0,6,12,18,24,30,36,90,96,102,108,114,120,126,132,138,144,150,160,165]],5),[cv2.IMWRITE_JPEG_QUALITY,92])
cv2.imwrite('v2_pip_1x.png',np.hstack([P[i][60:420,330:720] for i in [0,24,51,54,102,120]]))
# tremor: mean abs diff frame-to-frame in mouth ellipse box vs a cheek box
m=[float(np.abs(P[i+1][190:300,480:620].astype(int)-P[i][190:300,480:620]).mean()) for i in range(169)]
c=[float(np.abs(P[i+1][100:180,420:480].astype(int)-P[i][100:180,420:480]).mean()) for i in range(169)]
top=sorted(range(169),key=lambda k:-m[k])[:8]
print('mouth diff top',[(k,round(m[k],1)) for k in sorted(top)],'median',round(float(np.median(m)),1),'cheek med',round(float(np.median(c)),1))

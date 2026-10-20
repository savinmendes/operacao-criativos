import numpy as np,cv2
from fr import frames
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'
ts=[5.57,5.67,5.77,8.33,8.43,8.50,22.0,24.3,24.45,24.6,24.75,27.15,27.3,27.45,27.6,27.8]
want={int(round(t*30)) for t in ts}
r={}
for i,f in enumerate(frames(V)):
    if i in want: r[i]=f.copy()
    if i>max(want): break
ims=[lab(cv2.resize(r[i][330:560,230:500],(405,345)),f'{i/30:.2f}') for i in sorted(r)]
g=np.vstack([np.hstack(ims[k:k+4]) for k in range(0,16,4)])
cv2.imwrite('boca_pausas_telacheia.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,90])

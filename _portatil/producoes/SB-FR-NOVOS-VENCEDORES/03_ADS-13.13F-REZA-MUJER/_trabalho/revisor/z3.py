import numpy as np,cv2
from fr import frames
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'
want=[260,290,301,320,340,350,670,700,745,790,815,830]
r={}
for i,f in enumerate(frames(V)):
    if i in want: r[i]=f.copy()
    if i>max(want): break
ims=[]
for i in want:
    y0,y1=(700,850) if i<400 else (960,1120)
    ims.append(lab(cv2.resize(r[i][y0:y1],(1080,int((y1-y0)*1.5))),f'{i/30:.2f} y{y0}-{y1}'))
h=max(x.shape[0] for x in ims)
ims=[cv2.copyMakeBorder(x,0,h-x.shape[0],0,0,0) for x in ims]
g=np.vstack([np.hstack(ims[k:k+2]) for k in range(0,len(ims),2)])
cv2.imwrite('zoom_lama_abraco_cta.jpg',g,[cv2.IMWRITE_JPEG_QUALITY,90])

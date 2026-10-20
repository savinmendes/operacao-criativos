import numpy as np,cv2,sys
from fr import frames
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'; O=r'C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4'
def grab(path,idxs):
    d={}
    for i,f in enumerate(frames(path)):
        if i in idxs: d[i]=f.copy()
        if i>max(idxs): break
    return d
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
def grid(ims,cols):
    h,w=ims[0].shape[:2];rows=(len(ims)+cols-1)//cols
    g=np.zeros((rows*h,cols*w,3),np.uint8)
    for k,im in enumerate(ims): g[(k//cols)*h:(k//cols+1)*h,(k%cols)*w:(k%cols+1)*w]=im
    return g
# full frames overview every 1 s
idx=list(range(0,835,30))
d=grab(V,set(idx))
cv2.imwrite('ov_full.jpg',grid([lab(cv2.resize(d[i],(240,427)),f'{i/30:.1f}') for i in idx],7),[cv2.IMWRITE_JPEG_QUALITY,85])

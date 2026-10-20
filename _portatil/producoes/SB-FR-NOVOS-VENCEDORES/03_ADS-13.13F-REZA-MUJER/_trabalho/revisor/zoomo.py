import numpy as np,cv2
from fr import frames
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
def grid(ims,cols):
    h,w=ims[0].shape[:2];rows=(len(ims)+cols-1)//cols
    g=np.zeros((rows*h,cols*w,3),np.uint8)
    for k,im in enumerate(ims): g[(k//cols)*h:(k//cols+1)*h,(k%cols)*w:(k%cols+1)*w]=im
    return g
O=r'C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4'
L=[]
for i,f in enumerate(frames(O)):
    if i>=175: break
    L.append(f[830:940,480:620].copy())
ims=[lab(cv2.resize(L[i],None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC),f'ES {i/30:.2f}') for i in range(36,72,2)]
cv2.imwrite('orig_dedo_boca.jpg',grid(ims,6),[cv2.IMWRITE_JPEG_QUALITY,92])

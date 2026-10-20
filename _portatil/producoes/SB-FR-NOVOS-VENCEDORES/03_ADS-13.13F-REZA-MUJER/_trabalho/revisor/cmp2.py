import numpy as np,cv2
from fr import frames
def lab(im,t):
    im=im.copy();cv2.putText(im,t,(8,30),0,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),0,0.9,(0,255,255),2);return im
V='../../SB-FR-ADS-13.13F-REZA-MUJER.mp4'; O=r'C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4'
fi={301:'FR10.03',340:'FR11.33',680:'FR22.67',760:'FR25.33',820:'FR27.33'}
oi={330:'ES11.0',400:'ES13.33',800:'ES26.67',880:'ES29.33',930:'ES31.0'}
def g(p,d):
    r={}
    for i,f in enumerate(frames(p)):
        if i in d: r[i]=f.copy()
        if i>max(d): break
    return r
A=g(V,fi);B=g(O,oi)
rowA=[lab(cv2.resize(A[i][560:1280],(360,360)),fi[i]) for i in fi]
rowB=[lab(cv2.resize(B[i][560:1280],(360,360)),oi[i]) for i in oi]
cv2.imwrite('cmp_baixo_fr_vs_es.jpg',np.vstack([np.hstack(rowA),np.hstack(rowB)]),[cv2.IMWRITE_JPEG_QUALITY,90])

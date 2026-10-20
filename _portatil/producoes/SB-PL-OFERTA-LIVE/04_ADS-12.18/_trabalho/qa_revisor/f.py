import cv2, numpy as np
V=r"C:\Users\PICHAU\Downloads\SB-PL-OFERTA-LIVE\04_ADS-12.18\SB-PL-ADS-12.18.mp4"
cap=cv2.VideoCapture(V)
def fr(k):
    cap.set(cv2.CAP_PROP_POS_FRAMES,k); return cap.read()[1]
im=[cv2.resize(fr(k),(240,427)) for k in [75,315,318,321,830,900]]
for a,k in zip(im,[75,315,318,321,830,900]): cv2.putText(a,str(k),(5,25),0,0.8,(0,255,255),2)
cv2.imwrite("full.jpg",np.hstack(im))

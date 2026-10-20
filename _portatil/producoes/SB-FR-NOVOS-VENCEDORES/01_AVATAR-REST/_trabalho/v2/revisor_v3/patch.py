import cv2,numpy as np
from strips import grab
p='../SB-FR-AVATAR-REST_v3.mp4'
rng=list(range(1100,1120))+list(range(1505,1520))+list(range(1655,1670))+list(range(830,842))+list(range(1310,1320))
f=grab(p,rng)
# mouth region diff vs previous frame, region y 400-800 x 300-800
for i in rng[1:]:
    if i-1 in f:
        a=f[i-1][420:780,330:760].astype(float); b=f[i][420:780,330:760].astype(float)
        print(i, round(np.abs(a-b).mean(),1), end=' | ')
cv2.imwrite('fr/z1666.jpg', np.hstack([f[1665][200:1000,140:940], f[1666][200:1000,140:940]]))

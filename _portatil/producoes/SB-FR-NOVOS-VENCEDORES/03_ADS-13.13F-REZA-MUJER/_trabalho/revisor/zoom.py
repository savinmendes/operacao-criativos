import numpy as np,cv2
from sheet import lab,grid
P=np.load('F_pip.npy')  # y offset 640
def z(f,x0,y0,x1,y1,s=4): return cv2.resize(f[y0-640:y1-640,x0:x1],None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC)
# mouth region guess
ims=[lab(z(P[i],480,830,620,940,3),f'{i/30:.2f}') for i in range(39,63)]
cv2.imwrite('dedo_boca_1.3-2.1.jpg',grid(ims,6),[cv2.IMWRITE_JPEG_QUALITY,92])
ims=[lab(z(P[i],480,830,620,940,3),f'{i/30:.2f}') for i in [0,6,12,18,24,30,90,96,102,108,114,120,126,132,138,144,150,156,160,165]]
cv2.imwrite('boca_zoom.jpg',grid(ims,5),[cv2.IMWRITE_JPEG_QUALITY,92])

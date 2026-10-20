import cv2, numpy as np, time, warnings, sys
warnings.filterwarnings("ignore")
from simple_lama_inpainting import SimpleLama
from PIL import Image
sys.path.insert(0,'_tmp')
lama=SimpleLama(); BM=np.load("_tmp/boxmasks.npy")
def mascara_justa(roi):
    b, g, r = cv2.split(roi.astype(np.int16))
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    txt = ((np.minimum(r, g) > 150) & (gray > 150)).astype(np.uint8)
    txt &= cv2.dilate((gray < 80).astype(np.uint8), np.ones((7, 7), np.uint8))
    return cv2.dilate(txt, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
c=cv2.VideoCapture('../../../UNICOS_HD/11.mp4'); rows=[]
for t in [2.0,6.5,33.0,35.0]:
    c.set(0,t*1000); ok,f=c.read()
    crop=f[680:1136].copy()  # 456 tall
    fi=int(round(t*30)); m=np.zeros(crop.shape[:2],np.uint8); m[836-680:980-680]=cv2.dilate(BM[fi].astype(np.uint8),np.ones((7,7),np.uint8))
    t0=time.time()
    r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(m*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
    print(t, round(time.time()-t0,2))
    rows.append(np.hstack([crop[110:350],r[110:350]]))
cv2.imwrite('_tmp/lama.jpg',np.vstack(rows))

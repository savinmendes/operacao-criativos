import cv2, numpy as np, warnings
warnings.filterwarnings("ignore")
from simple_lama_inpainting import SimpleLama
from PIL import Image
BM=np.load('_tmp/boxmasks.npy'); Y0,Y1=836,980; A,B=0,265
cap=cv2.VideoCapture('../../../UNICOS_HD/11.mp4'); fr=[]
for i in range(B):
    ok,f=cap.read(); fr.append(f[600:1220].copy())
st=np.stack(fr).astype(np.float32)
for k in range(B):
    st[k, Y0-600:Y1-600][BM[k].astype(bool)] = np.nan
p=np.nanmedian(st,axis=0); hole=np.isnan(p).any(2)
p=np.nan_to_num(p).astype(np.uint8)
hole=cv2.dilate(hole.astype(np.uint8),np.ones((7,7),np.uint8))
print('holes',hole.sum())
lama=SimpleLama()
res=lama(Image.fromarray(cv2.cvtColor(p,cv2.COLOR_BGR2RGB)),Image.fromarray(hole*255))
res=cv2.cvtColor(np.array(res),cv2.COLOR_RGB2BGR)[:p.shape[0],:p.shape[1]]
np.save('_tmp/placa_menina.npy',res[Y0-600:Y1-600])
cv2.imwrite('_tmp/placa_menina.jpg',np.vstack([p,res]))

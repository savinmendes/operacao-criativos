"""Refaz a remoção da legenda nos quadros 286-305 (clarão da transição menina -> Desatadora, onde a máscara por cor falha):
máscara = caixa do texto (x 90-600, y 860-955) somada à máscara antiga."""
import cv2, numpy as np, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
R0,R1=840,1210; C0,C1=760,1240
lama=SimpleLama(); cap=cv2.VideoCapture('../../../UNICOS_HD/04.mp4'); cap.set(1,286)
for i in range(286,306):
    ok,f=cap.read(); m=np.zeros((1280,720),np.uint8); m[R0:R1]=np.load(f'_tmp/mask/{i:04d}.npy'); m[860:955,90:600]=1
    np.save(f'_tmp/mask/{i:04d}.npy',m[R0:R1])
    crop=f[C0:C1].copy(); r=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(m[C0:C1]*255))
    r=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]; cv2.imwrite(f'_tmp/lama/{i:04d}.png',r[R0-C0:R1-C0])
print("ok")

# RapidOCR só detecção, quadro a quadro, faixa y 950-1720 (1080x1920) -> ocr_boxes.json
import cv2, json, numpy as np, time
from rapidocr_onnxruntime import RapidOCR
from comum3 import quadros
ocr=RapidOCR(); Y0,Y1=950,1720; res={}; t0=time.time(); N=2151
for i,f in enumerate(quadros("fontes/es.mp4",w=1080,h=1920)):
    r,_=ocr(f[Y0:Y1],use_det=True,use_cls=False,use_rec=False)
    bx=[]
    for b in (r or []):
        b=np.array(b); x0,y0=b.min(0); x1,y1=b.max(0); bx.append([int(x0),int(y0+Y0),int(x1),int(y1+Y0)])
    res[i]=bx
    if i%100==0: print(f"[{i}/{N}] {100*i//N}% falta ~{(time.time()-t0)/(i+1)*(N-i):.0f}s", bx[:3], flush=True)
json.dump(res,open("ocr_boxes.json","w"))
print("ok",i+1)

# detecção de texto (RapidOCR só det) quadro a quadro na faixa y 600-1150 -> caixas de legenda por quadro
import cv2, json, numpy as np, time, sys
from rapidocr_onnxruntime import RapidOCR
ocr=RapidOCR(); cap=cv2.VideoCapture("fontes/es.mp4"); N=int(cap.get(7)); Y0,Y1=600,1150
res={}; t0=time.time(); i=0; t1=time.time()
r,_=ocr(np.zeros((100,100,3),np.uint8),use_det=True,use_cls=False,use_rec=False)
while True:
    ok,f=cap.read()
    if not ok: break
    r,_=ocr(f[Y0:Y1],use_det=True,use_cls=False,use_rec=False)
    bx=[]
    for b in (r or []):
        b=np.array(b); x0,y0=b.min(0); x1,y1=b.max(0)
        bx.append([int(x0),int(y0+Y0),int(x1),int(y1+Y0),"det",1.0])
    res[i]=bx
    if i%50==0: print(f"[{i}/{N}] falta ~{(time.time()-t0)/(i+1)*(N-i):.0f}s", bx[:2], flush=True)
    i+=1
json.dump(res,open("ocr_boxes.json","w",encoding="utf-8"),ensure_ascii=False)
print("ok",i)

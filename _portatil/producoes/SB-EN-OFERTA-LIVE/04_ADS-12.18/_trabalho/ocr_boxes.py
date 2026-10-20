# Detecta caixas de texto (legenda ES queimada) por quadro, na faixa Y0..Y1. Saida: ocr_boxes.json {quadro: [[x0,y0,x1,y1],...]}
import cv2, json, sys, time, numpy as np
from rapidocr_onnxruntime import RapidOCR
Y0,Y1=560,1180
eng=RapidOCR(intra_op_num_threads=6,inter_op_num_threads=1)
cap=cv2.VideoCapture("../original/SB-ES_ADS-12.18.mp4"); N=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
out={}; t0=time.time()
STEP=5
for i in range(N):
    ok,f=cap.read()
    if not ok: break
    if i%STEP: continue
    roi=f[Y0:Y1]
    res,_=eng(roi,use_det=True,use_cls=False,use_rec=False)
    bx=[]
    for b in (res or []):
        p=np.array(b); x0,y0=p.min(0); x1,y1=p.max(0)
        if (y1-y0)<18 or (x1-x0)<20: continue
        bx.append([int(x0),int(y0+Y0),int(x1),int(y1+Y0)])
    out[i]=bx
    if i%50==0: print(i,N,bx,f"{time.time()-t0:.0f}s",flush=True)
json.dump(out,open("ocr_boxes.json","w"))

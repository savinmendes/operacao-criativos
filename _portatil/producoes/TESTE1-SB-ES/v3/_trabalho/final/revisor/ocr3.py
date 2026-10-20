import cv2,json
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR();res=[]
jobs=[(0,1653,9,505,560),(3090,3300,9,430,495),(3530,3710,9,430,495),(4660,5085,9,395,450)]
for a,b,s,y0,y1 in jobs:
    for i in range(a,b,s):
        im=cv2.resize(cv2.imread(f'f/{i:05d}.jpg')[y0:y1],None,fx=2,fy=2)
        r,_=o(im)
        txt=' '.join(t[1] for t in (r or []) if 'TOCA' not in t[1] and float(t[2])>0.5)
        res.append((i,txt));print(f'{i/30:6.2f} {txt}',flush=True)
json.dump(res,open('ocr3.json','w',encoding='utf-8'),ensure_ascii=False)

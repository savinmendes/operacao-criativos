import cv2,json,numpy as np,sys
from rapidocr_onnxruntime import RapidOCR
def mask(i):
    im=cv2.imread(f'f/{i:05d}.jpg')[420:585].astype(int)
    b,g,r=im[...,0],im[...,1],im[...,2]
    m=((b>215)&(g>215)&(r>215))|((r>200)&(g>190)&(b<110))
    return m
keys=[];prev=None
for i in range(5085):
    m=mask(i)
    if prev is None: keys.append(i)
    else:
        inter=(m&prev).sum();uni=(m|prev).sum()
        if uni>30 and inter/uni<0.6: keys.append(i)
    prev=m
print('keys',len(keys),flush=True)
o=RapidOCR();res=[]
for n,k in enumerate(keys):
    j=min(k+2,5084)
    im=cv2.resize(cv2.imread(f'f/{j:05d}.jpg')[420:585],None,fx=2,fy=2)
    r,_=o(im)
    txt=' '.join(t[1] for t in (r or []) if 'TOCA' not in t[1] and 'VER' not in t[1] and float(t[2])>0.5)
    res.append((k,txt))
    if n%20==0: print(n,flush=True)
json.dump(res,open('ocr2.json','w',encoding='utf-8'),ensure_ascii=False)

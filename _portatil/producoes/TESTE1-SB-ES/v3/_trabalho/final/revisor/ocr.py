import cv2,json
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR();res=[]
prev=None;last=''
for i in range(0,5085,3):
    im=cv2.imread(f'f/{i:05d}.jpg')[420:585]
    im=cv2.resize(im,None,fx=2,fy=2)
    r,_=o(im)
    txt=' '.join(t[1] for t in (r or []) if 'TOCA' not in t[1] and 'VER' not in t[1] and float(t[2])>0.6)
    res.append((i,txt))
json.dump(res,open('ocr.json','w',encoding='utf-8'),ensure_ascii=False)
# compress
seq=[];
for i,t in res:
    if not seq or seq[-1][2]!=t: seq.append([i,i,t])
    else: seq[-1][1]=i
for a,b,t in seq: print(f'{a/30:7.2f}-{b/30:7.2f} {t}')

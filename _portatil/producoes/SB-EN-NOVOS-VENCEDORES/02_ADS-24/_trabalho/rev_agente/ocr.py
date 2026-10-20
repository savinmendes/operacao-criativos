import glob,json,os
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR(); res=[]
for i,f in enumerate(sorted(glob.glob("f05/*.jpg"))):
    t=(i)/2+0.25
    r,_=o(f)
    items=[(round(min(p[1] for p in b)),round(max(p[1] for p in b)),txt,round(float(c),2)) for b,txt,c in (r or [])]
    res.append((t,items))
    print(f"{t:6.2f}", " | ".join(f"y{a}-{b}:{txt}({c})" for a,b,txt,c in items))
json.dump(res,open("ocr.json","w"),ensure_ascii=False)

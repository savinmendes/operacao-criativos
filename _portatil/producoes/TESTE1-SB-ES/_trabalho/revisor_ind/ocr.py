import glob,json,cv2
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR(); out=[]
for i,f in enumerate(sorted(glob.glob('f2/*.jpg'))):
    t=i*0.5+0.25
    im=cv2.imread(f); rec=[]
    r,_=o(im)
    for b,txt,c in (r or []): rec.append(('full',int(b[0][1]),txt,round(float(c),2)))
    for name,(y0,y1) in {'top':(0,330),'band':(800,1080),'low':(1050,1280)}.items():
        z=cv2.resize(im[y0:y1],None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
        r,_=o(z)
        for b,txt,c in (r or []): rec.append((name,int(b[0][1]/2+y0),txt,round(float(c),2)))
    out.append({'t':t,'r':rec})
    print(f"{t:6.2f} | "+" | ".join(sorted(set(x[2] for x in rec))),flush=True)
json.dump(out,open('ocr.json','w',encoding='utf-8'),ensure_ascii=False)

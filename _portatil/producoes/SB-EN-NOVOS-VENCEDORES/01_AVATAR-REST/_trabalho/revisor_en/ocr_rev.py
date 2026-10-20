import sys,json,re,numpy as np,cv2
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho")
from comum3 import quadros
from rapidocr_onnxruntime import RapidOCR
v=r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\SB-EN-AVATAR-REST_v2.mp4"
ass=open(r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\leg_en.ass",encoding="utf-8").read()
def t2s(t):h,m,s=t.split(":");return int(h)*3600+int(m)*60+float(s)
mids=[]
for m in re.finditer(r"Dialogue: 0,([\d:.]+),([\d:.]+),",ass):
    a,b=t2s(m.group(1)),t2s(m.group(2)); mids.append((a+b)/2)
want=sorted(set([round(i*15) for i in range(114)]+[round(t*30) for t in mids if t<56.7]))
want=[w for w in want if w<1701]
eng=RapidOCR(); res={}
ws=set(want)
for i,f in enumerate(quadros(v,w=1080,h=1920)):
    if i not in ws: continue
    r,_=eng(f)
    res[i]=[[t,round(float(c),2),[int(min(p[0] for p in b)),int(min(p[1] for p in b)),int(max(p[0] for p in b)),int(max(p[1] for p in b))]] for b,t,c in (r or [])]
    print(i,round(i/30,2)," | ".join(x[0] for x in res[i]),flush=True)
json.dump(res,open("ocr.json","w",encoding="utf-8"),ensure_ascii=False)

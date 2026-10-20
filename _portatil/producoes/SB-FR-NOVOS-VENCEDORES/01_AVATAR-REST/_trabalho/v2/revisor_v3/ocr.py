import cv2,json
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR(); cap=cv2.VideoCapture('../SB-FR-AVATAR-REST_v3.mp4'); i=0; res=[]
while True:
    ok,f=cap.read()
    if not ok: break
    if i%10==0:
        r,_=o(f)
        txt=[t[1] for t in (r or []) if t[2]>0.6]
        res.append((i,round(i/30,2),txt)); print(i,round(i/30,2),' | '.join(txt),flush=True)
    i+=1
json.dump(res,open('ocr.json','w',encoding='utf-8'),ensure_ascii=False)

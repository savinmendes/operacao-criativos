import subprocess,numpy as np,json,sys
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR()
V="v2.mp4"
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-vf','fps=2','-pix_fmt','bgr24','-f','rawvideo','-'],stdout=subprocess.PIPE)
out=[];i=0;n=1280*720*3
while True:
    b=p.stdout.read(n)
    if len(b)<n: break
    f=np.frombuffer(b,np.uint8).reshape(1280,720,3)
    r,_=o(f); out.append((i/2,[x[1] for x in (r or [])])); i+=1
    if i%40==0: print(i,flush=True)
json.dump(out,open('ocr.json','w',encoding='utf8'),ensure_ascii=False)
print('ok',i)

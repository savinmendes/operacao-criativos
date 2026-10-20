import subprocess,numpy as np,json,re,sys
from rapidocr_onnxruntime import RapidOCR
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
ocr=RapidOCR()
def stream(fps,crop):
    W,H=crop[0],crop[1]
    p=subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf",f"fps={fps},crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    i=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield i/fps,np.frombuffer(b,np.uint8).reshape(H,W,3); i+=1
mode=sys.argv[1]
out=[]
if mode=='top':
    gen=stream(2,(720,70,0,0))
else:
    gen=stream(1,(720,280,0,680))
for t,img in gen:
    r,_=ocr(img)
    txt=[(x[1],round(float(x[2]),2)) for x in (r or [])]
    out.append((t,txt))
    if int(t)%120==0 and (t%1==0): print(mode,t,txt,flush=True)
json.dump(out,open(f"ocr_{mode}.json","w",encoding="utf-8"),ensure_ascii=False)
print("DONE",mode)

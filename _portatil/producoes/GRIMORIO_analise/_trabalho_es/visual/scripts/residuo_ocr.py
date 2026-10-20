import sys, subprocess, numpy as np, json
from rapidocr_onnxruntime import RapidOCR
e = RapidOCR()
V, RNG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BANDAS = [(0, 239, 625, 725), (232, 668, 1010, 1110), (657, 2290, 725, 880), (2279, 2628, 870, 975), (2616, 4645, 725, 880)]
p = subprocess.Popen(["ffmpeg","-v","error","-i",V,"-vf",f"scale=in_color_matrix=bt709:in_range={RNG},format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
T=720*1280*3; i=0; res=[]
while True:
    b=p.stdout.read(T)
    if len(b)<T: break
    if i%6==0:
        f=np.frombuffer(b,np.uint8).reshape(1280,720,3)
        r,_=e(f)
        for q,tx,c in (r or []):
            q=np.array(q); cy=(q[:,1].min()+q[:,1].max())/2; h=q[:,1].max()-q[:,1].min()
            if any(a<=i<bb and y0-10<=cy<=y1+10 for a,bb,y0,y1 in BANDAS) and h>=26 and c>0.6:
                res.append([i, round(i/30,2), tx, round(float(c),2), [int(q[:,0].min()),int(q[:,1].min()),int(q[:,0].max()),int(q[:,1].max())]])
    i+=1
json.dump(res,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=0); print(len(res))

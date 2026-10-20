import subprocess, io, sys, json, glob
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
A = r"C:/Users/PICHAU/Downloads/LHYMPORIA AD 01-20/lymphoria/_trabalho/"
U = r"C:/Users/PICHAU/Downloads/DRENAGEM-LATAM/producao/_trabalho/ugc/prod/"
fs = sys.argv[1:]
LABEL = {"lymphoria","drenaje","linfático","linfatico","apoyo","extractos","herbales","suplemento","dietético","oz","liq","ml","tradicional","líquidos","liquidos","sabe","miel","linfático tradicional"}
for f in fs:
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    hits=[]; t=0.05
    while t < d-0.05:
        p = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",f,"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        im = np.array(Image.open(io.BytesIO(p)).convert("RGB"))
        r,_ = ocr(im)
        for box,txt,sc in (r or []):
            if sc<0.6: continue
            w=[x for x in txt.lower().replace(","," ").replace(".", " ").split() if x]
            if len(w)>=2 and any(c.islower() for c in txt) and len(txt)>=8 and not any(k in txt.lower() for k in ("drenaje","linf","oz","extract","suple","apoyo")):
                hits.append((round(t,2),txt))
        t+=0.3
    print(f.split("/")[-3:] , "OK" if not hits else hits[:8], flush=True)

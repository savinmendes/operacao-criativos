import glob
from rapidocr_onnxruntime import RapidOCR
o=RapidOCR(); prev=None; out=[]
for i,f in enumerate(sorted(glob.glob("cap/*.png"))):
    r,_=o(f); t=" ".join(x[1] for x in (r or []))
    if t!=prev: out.append(f"{i/10:.1f}  {t}"); prev=t
open("ocr.txt","w",encoding="utf-8").write("\n".join(out))

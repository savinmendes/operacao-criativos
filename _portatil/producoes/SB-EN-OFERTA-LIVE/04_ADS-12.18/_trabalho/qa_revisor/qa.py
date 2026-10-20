import subprocess, json, os, sys
D=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\04_ADS-12.18"
V=D+r"\SB-EN-ADS-12.18.mp4"; Q=D+r"\_trabalho\qa_revisor"
fr=Q+r"\fr"; os.makedirs(fr,exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",V,"-vf","fps=4","-start_number","0",fr+r"\f%04d.png"],check=True)
from rapidocr_onnxruntime import RapidOCR
ocr=RapidOCR(); out=[]
for f in sorted(os.listdir(fr)):
    i=int(f[1:5]); t=(i)/4+0.125
    r,_=ocr(os.path.join(fr,f))
    items=[[round(t,3),[int(min(p[0] for p in b)),int(min(p[1] for p in b)),int(max(p[0] for p in b)),int(max(p[1] for p in b))],s,round(c,2)] for b,s,c in (r or [])]
    out.append(items)
    print(t, [(x[2],x[1][1],x[3]) for x in items], flush=True)
json.dump(out,open(Q+r"\ocr.json","w",encoding="utf-8"),ensure_ascii=False)
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
for lang in ["en"]:
    segs,_=m.transcribe(V,language=lang,word_timestamps=True)
    W=[]
    for s in segs:
        print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}",flush=True)
        for w in s.words: W.append([round(w.start,2),round(w.end,2),w.word,round(w.probability,2)])
    json.dump(W,open(Q+rf"\words_{lang}.json","w",encoding="utf-8"),ensure_ascii=False)
    print(" ".join(f"{w[2].strip()}@{w[0]}-{w[1]}({w[3]})" for w in W))

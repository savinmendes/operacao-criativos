import json,sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe(r"C:\Users\PICHAU\Downloads\SB-COLAR-BREVIARIO-ES\original_wsen5drS7Nk.mp4",language="pt",word_timestamps=True)
out=[];txt=[]
for s in segs:
    out.append({"ini":s.start,"fim":s.end,"texto":s.text,"palavras":[[w.word,w.start,w.end] for w in s.words]})
    txt.append(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")
open(r"C:\Users\PICHAU\Downloads\SB-COLAR-BREVIARIO-ES\_trabalho\transcricao_pt.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1))
open(r"C:\Users\PICHAU\Downloads\SB-COLAR-BREVIARIO-ES\_trabalho\transcricao_pt.txt","w",encoding="utf-8").write("\n".join(txt))
print("\n".join(txt))

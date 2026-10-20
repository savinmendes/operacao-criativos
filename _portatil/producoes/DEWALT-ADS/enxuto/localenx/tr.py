import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for n in ["32","48"]:
    segs,_=m.transcribe(f"a{n}.wav",language="es",word_timestamps=True)
    out=[]
    for s in segs:
        out.append({"s":round(s.start,2),"e":round(s.end,2),"t":s.text,"w":[(round(w.start,2),round(w.end,2),w.word) for w in s.words]})
        print(n,round(s.start,2),round(s.end,2),s.text)
    json.dump(out,open(f"tr{n}.json","w",encoding="utf-8"),ensure_ascii=False)

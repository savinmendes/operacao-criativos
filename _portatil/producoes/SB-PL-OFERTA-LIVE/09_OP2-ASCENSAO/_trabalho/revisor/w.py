import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],language="pl",word_timestamps=True,vad_filter=False)
out=[]
for s in segs:
    for w in s.words: out.append((round(w.start,2),round(w.end,2),w.word))
json.dump(out,open("words.json","w",encoding="utf-8"),ensure_ascii=False)
for o in out: print(o)

import sys,subprocess,json
from faster_whisper import WhisperModel
v=sys.argv[1]
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,info=m.transcribe(v,language="pl",word_timestamps=True)
out=[]
for s in segs:
    for w in s.words: out.append((round(w.start,2),round(w.end,2),w.word))
print(" ".join(w for _,_,w in out))
for a,b,w in out: print(a,b,w)

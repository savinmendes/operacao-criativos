import json,sys
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=8)
segs,_=m.transcribe(sys.argv[1],language=sys.argv[2],word_timestamps=True)
out=[]
for s in segs:
    for w in s.words: out.append([round(w.start,2),round(w.end,2),w.word])
    print(f"{s.start:.2f}-{s.end:.2f} {s.text}")
json.dump(out,open(sys.argv[3],"w",encoding="utf-8"),ensure_ascii=False)

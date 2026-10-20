from faster_whisper import WhisperModel
import json,sys
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe(sys.argv[1],language="en",word_timestamps=True)
out=[]
for s in segs:
    for w in s.words: out.append((round(w.start,2),round(w.end,2),w.word))
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
json.dump(out,open("words.json","w"))

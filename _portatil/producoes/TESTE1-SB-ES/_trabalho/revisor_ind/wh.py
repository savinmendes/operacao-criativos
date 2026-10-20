import sys,json
from faster_whisper import WhisperModel
lang=sys.argv[1]; out=sys.argv[2]
m=WhisperModel(sys.argv[3] if len(sys.argv)>3 else "medium",device="cpu",compute_type="int8")
segs,_=m.transcribe("audio.wav",language=lang,word_timestamps=True,beam_size=5,vad_filter=False)
res=[]
for s in segs:
    res.append({"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word,w.probability) for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}",flush=True)
json.dump(res,open(out,"w",encoding="utf-8"),ensure_ascii=False)

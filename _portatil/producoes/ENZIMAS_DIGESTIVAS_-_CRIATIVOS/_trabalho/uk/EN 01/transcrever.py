import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv)>2 else "medium", device="cpu", compute_type="int8", cpu_threads=8)
segs, _ = m.transcribe(sys.argv[1], language="en", word_timestamps=True, beam_size=5)
out=[]
for s in segs:
    ws=[{"w":w.word,"s":round(w.start,2),"e":round(w.end,2)} for w in s.words]
    out.append({"s":round(s.start,2),"e":round(s.end,2),"t":s.text,"words":ws})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", flush=True)
json.dump(out, open(sys.argv[3] if len(sys.argv)>3 else "transcricao.json","w",encoding="utf-8"), ensure_ascii=False, indent=0)

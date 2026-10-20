import sys, json
from faster_whisper import WhisperModel
src, lang, out = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(src, language=lang, word_timestamps=True)
res=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    for w in s.words: res.append({"w":w.word.strip(),"s":round(w.start,2),"e":round(w.end,2)})
json.dump(res, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=0)
print(" ".join(f"{r['w']}@{r['s']}" for r in res))

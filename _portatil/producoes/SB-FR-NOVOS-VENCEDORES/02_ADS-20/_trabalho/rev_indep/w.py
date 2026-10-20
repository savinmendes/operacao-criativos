import json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,info=m.transcribe("a.wav",language="fr",word_timestamps=True,vad_filter=False)
out=[]
for s in segs:
    for w in s.words: out.append([round(w.start,2),round(w.end,2),w.word.strip(),round(w.probability,2)])
json.dump(out,open("words.json","w",encoding="utf-8"),ensure_ascii=False)
print(" ".join(w[2] for w in out))

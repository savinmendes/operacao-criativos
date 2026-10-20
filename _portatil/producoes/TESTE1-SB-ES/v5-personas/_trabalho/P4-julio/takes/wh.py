import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small", device="cpu", compute_type="int8")
seg, _ = m.transcribe(sys.argv[1], language="es", word_timestamps=True)
W=[]
for s in seg:
    for w in s.words: W.append(dict(w=w.word.strip(), ini=round(w.start,2), fim=round(w.end,2), p=round(w.probability,2)))
print(json.dumps(W, ensure_ascii=False))

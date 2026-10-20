import sys, json
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(src, language="pt", word_timestamps=True, vad_filter=False)
W = []
for s in segs:
    for w in s.words: W.append([round(w.start,2), round(w.end,2), w.word.strip()])
json.dump(W, open(out,"w",encoding="utf-8"), ensure_ascii=False)

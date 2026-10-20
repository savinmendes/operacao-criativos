import sys, json, os
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=8)
src = sys.argv[1]; out = sys.argv[2]
res = {}
for f in sorted(os.listdir(src)):
    if not f.endswith(".mp4"): continue
    segs, _ = m.transcribe(os.path.join(src, f), language="es", word_timestamps=True, vad_filter=False)
    ws = []
    for s in segs:
        for w in s.words: ws.append([round(w.start,2), round(w.end,2), w.word.strip()])
    res[f] = ws
    print(f, len(ws), flush=True)
json.dump(res, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=0)

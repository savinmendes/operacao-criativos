import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], language="es", word_timestamps=True, vad_filter=False)
W = [dict(w=w.word.strip(), ini=round(w.start, 2), fim=round(w.end, 2), p=round(w.probability, 2)) for s in segs for w in s.words]
print(" ".join(f"{x['w']}[{x['ini']}-{x['fim']}]" for x in W))
json.dump(W, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)

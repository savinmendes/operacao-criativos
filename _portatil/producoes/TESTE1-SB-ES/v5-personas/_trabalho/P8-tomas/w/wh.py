import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "small", device="cpu", compute_type="int8")
seg, _ = m.transcribe(sys.argv[1], language="es", word_timestamps=True)
W = []
for s in seg:
    for w in s.words: W.append(dict(w=w.word.strip(), ini=round(w.start, 2), fim=round(w.end, 2), p=round(w.probability, 2)))
print(" ".join(f"{x['w']}[{x['ini']}]" for x in W))
if len(sys.argv) > 3: json.dump(W, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=0)

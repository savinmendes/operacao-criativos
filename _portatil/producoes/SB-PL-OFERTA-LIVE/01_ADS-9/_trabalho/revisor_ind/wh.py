import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,info=m.transcribe(sys.argv[1],language="pl",word_timestamps=True,beam_size=5)
with open(sys.argv[2],"w",encoding="utf-8") as f:
  for s in segs:
    f.write(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}\n")
    f.write("   "+" ".join(f"{w.word.strip()}({w.start:.2f},{w.probability:.2f})" for w in s.words)+"\n")

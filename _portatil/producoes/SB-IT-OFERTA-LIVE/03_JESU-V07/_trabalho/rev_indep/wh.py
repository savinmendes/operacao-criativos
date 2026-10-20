import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=4)
segs,info=m.transcribe(sys.argv[1],language="it",word_timestamps=True,beam_size=5)
with open(sys.argv[2],"w",encoding="utf-8") as f:
  for s in segs:
    f.write(f"[{s.start:.2f}-{s.end:.2f}] {s.text}\n")
    for w in s.words: f.write(f"   {w.start:6.2f}-{w.end:6.2f} {w.probability:.2f} {w.word}\n")

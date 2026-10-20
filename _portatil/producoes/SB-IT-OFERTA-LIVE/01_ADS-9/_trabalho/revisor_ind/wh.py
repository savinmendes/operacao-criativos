import sys
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=8) if True else None
segs,info=m.transcribe(sys.argv[1],language="it",word_timestamps=True,beam_size=5)
out=open(sys.argv[2],"w",encoding="utf-8")
for s in segs:
    out.write(f"{s.start:6.2f}-{s.end:6.2f} {s.text}\n")
    for w in s.words:
        if w.probability<0.6: out.write(f"   LOWP {w.start:.2f} {w.word!r} {w.probability:.2f}\n")
out.close()

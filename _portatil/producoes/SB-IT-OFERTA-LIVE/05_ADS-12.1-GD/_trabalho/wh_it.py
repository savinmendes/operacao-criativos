import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
seg,_=m.transcribe(sys.argv[1],language="it",word_timestamps=False)
for s in seg: print(f"{s.start:.2f}-{s.end:.2f} {s.text}")

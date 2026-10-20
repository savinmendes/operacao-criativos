import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
seg,info=m.transcribe(sys.argv[1],language=None)
print("lang",info.language,round(info.language_probability,3))
for s in seg: print(f"{s.start:.2f}-{s.end:.2f} {s.text}")

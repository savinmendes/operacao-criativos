import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for p in sys.argv[1:]:
    seg,info=m.transcribe(p,language=None,beam_size=5)
    print(p,info.language,round(info.language_probability,2),"|"," ".join(s.text.strip() for s in seg))

import sys
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for p in sys.argv[1:]:
    s,info=m.transcribe(p,language="it")
    print(p, ' '.join(x.text.strip() for x in s))
    s,info=m.transcribe(p)
    print('  lang detect:',info.language,round(info.language_probability,2))

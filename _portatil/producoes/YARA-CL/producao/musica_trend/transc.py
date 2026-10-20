import sys, json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for f in sys.argv[1:]:
    lang = "en" if "bambam" in f else "es"
    segs,_=m.transcribe(f,language=lang,word_timestamps=False,vad_filter=False)
    print("=====",f)
    for s in segs: print(f"{s.start:6.1f}-{s.end:6.1f} {s.text}")

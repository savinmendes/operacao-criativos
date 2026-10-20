import sys
from faster_whisper import WhisperModel
for name in ["small","medium"]:
    try: m=WhisperModel(name,device="cpu",compute_type="int8",local_files_only=True)
    except Exception as e: print(name,"indisp",type(e).__name__); continue
    for f in ["cta.wav","rien.wav"]:
        s,_=m.transcribe(f,language="fr",beam_size=5,word_timestamps=True)
        print(name,f,[(round(w.start,2),w.word,round(w.probability,2)) for x in s for w in x.words])

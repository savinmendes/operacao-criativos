from faster_whisper import WhisperModel
import numpy as np,wave
for name in ["small","medium"]:
    m=WhisperModel(name,device="cpu",compute_type="int8",local_files_only=True)
    s,_=m.transcribe("r2/cta.wav",language="fr",beam_size=5,word_timestamps=True)
    print(name," ".join(f"{w.word.strip()}[{122.5+w.start:.2f}|{w.probability:.2f}]" for x in s for w in x.words))
w=wave.open("r2/cta.wav");x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
print(" ".join(f"{122.5+i*0.1:.1f}:{20*np.log10(np.sqrt((x[int(i*1600):int((i+1)*1600)]**2).mean())+1):.0f}" for i in range(140)))

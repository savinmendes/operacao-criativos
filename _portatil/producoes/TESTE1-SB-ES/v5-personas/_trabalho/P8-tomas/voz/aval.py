import sys, numpy as np, subprocess
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
import librosa
for f in sys.argv[1:]:
    seg,_=m.transcribe(f,language="es"); t=" ".join(s.text for s in seg)
    y,sr=librosa.load(f,sr=16000); f0,v,_=librosa.pyin(y,fmin=60,fmax=300,sr=sr)
    print(f, "F0med",round(float(np.nanmedian(f0)),1),"| ",t)

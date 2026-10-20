import subprocess, tempfile, numpy as np
from pathlib import Path
from resemblyzer import VoiceEncoder, preprocess_wav
enc=VoiceEncoder(verbose=False); t=Path(tempfile.mkdtemp())
def emb(src,de,ate,n):
    o=t/f"{n}.wav"; subprocess.run(["ffmpeg","-v","error","-y","-ss",str(de),"-to",str(ate),"-i",src,"-ac","1","-ar","16000",str(o)],check=True)
    return enc.embed_utterance(preprocess_wav(o))
a=emb(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\04.mp4",44,110,"a")
b=emb(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\AD 02.mp4",44,110,"b")
c=emb(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad02\narr_fim.mp3",0,25,"c")
print("04 vs AD02 orig", float(np.dot(a,b)), " 04 vs clone02 gerado", float(np.dot(a,c)))

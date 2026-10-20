import subprocess, tempfile, numpy as np
from pathlib import Path
from resemblyzer import VoiceEncoder, preprocess_wav
S=Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20"); L=S/"lymphoria"/"_trabalho"
enc=VoiceEncoder(verbose=False); tmp=Path(tempfile.mkdtemp())
def emb(src,de=None,ate=None,n="x"):
    o=tmp/f"{n}.wav"; c=["-ss",str(de),"-to",str(ate)] if de is not None else []
    subprocess.run(["ffmpeg","-v","error","-y",*c,"-i",str(src),"-ac","1","-ar","16000",str(o)],check=True)
    return enc.embed_utterance(preprocess_wav(o))
ref=emb(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\24.mp4",180,300,"ref")
for nm,src,de,ate in [("AD13 orig",S/"AD 13.mp4",60,180),("AD14 orig",S/"AD 14.mp4",60,180),("AD13 clone",L/"ad13"/"narr_fim.mp3",None,None),("AD14 clone",L/"ad14"/"narr_fim.mp3",None,None),("AD04 clone",L/"ad04"/"narr_fim_univ.mp3",None,None),("AD02 orig",S/"AD 02.mp4",30,120),("AD24self",r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\24.mp4",400,500)]:
    try: print(nm, round(float(np.dot(ref,emb(src,de,ate,nm.replace(' ','')))),3))
    except Exception as e: print(nm,"erro",e)

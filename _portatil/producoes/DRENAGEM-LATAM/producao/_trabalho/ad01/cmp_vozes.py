import subprocess, tempfile, glob
from pathlib import Path
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
L = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de=None, ate=None, n="x"):
    o = tmp/f"{n}.wav"; c = ["-ss",str(de),"-to",str(ate)] if de is not None else []
    subprocess.run(["ffmpeg","-v","error","-y",*c,"-i",str(src),"-ac","1","-ar","16000",str(o)],check=True)
    return enc.embed_utterance(preprocess_wav(o))
o = emb(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais\01.mp4", 120, 240, "o")
for d in sorted(L.glob("ad*")):
    v = (d/"voz.txt").read_text().strip() if (d/"voz.txt").exists() else ("FNIhgYgEcJsdWbHRFiz6" if d.name=="ad04" else "?")
    f = d/"narr_fim.mp3"
    if d.name=="ad04": f = d/"narr_fim_univ.mp3"
    if f.exists(): print(d.name, v, f"{float(np.dot(o, emb(f, n=d.name))):.3f}")

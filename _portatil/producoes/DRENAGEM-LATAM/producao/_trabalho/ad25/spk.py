import subprocess, tempfile, sys, numpy as np
from pathlib import Path
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de, ate, n):
    o = tmp / f"{n}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(de),"-to",str(ate),"-i",src,"-ac","1","-ar","16000",str(o)],check=True)
    return enc.embed_utterance(preprocess_wav(o))
src = sys.argv[1]; E = {}
for s in sys.argv[2:]:
    x = s.split("|"); E[x[0]] = emb(x[3] if len(x) > 3 else src, float(x[1]), float(x[2]), x[0])
ks = list(E); base = [k for k in ks if "|" not in k][:3]
print("      " + " ".join(f"{k[:6]:>6}" for k in ks))
for k in ks: print(f"{k[:6]:>6}", " ".join(f"{float(np.dot(E[k],E[j])):6.2f}" for j in ks))

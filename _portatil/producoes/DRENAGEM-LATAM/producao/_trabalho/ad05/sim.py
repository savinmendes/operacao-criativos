import subprocess, tempfile, sys
from pathlib import Path
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de=None, ate=None, n="x"):
    o = tmp / f"{n}.wav"; c = ["-ss", str(de), "-to", str(ate)] if de is not None else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c, "-i", str(src), "-ac", "1", "-ar", "16000", str(o)], check=True)
    return enc.embed_utterance(preprocess_wav(o))
r = emb(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), "r")
for g in sys.argv[4:]: print(g, "%.3f" % float(np.dot(r, emb(g, n=Path(g).stem))))

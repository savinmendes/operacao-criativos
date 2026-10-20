# -*- coding: utf-8 -*-
import subprocess, tempfile, sys
from pathlib import Path
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
L = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de=None, ate=None, n="x"):
    o = tmp / f"{n}.wav"; c = ["-ss", str(de), "-to", str(ate)] if de is not None else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c, "-i", str(src), "-ac", "1", "-ar", "16000", str(o)], check=True)
    return enc.embed_utterance(preprocess_wav(o))
src, de, ate = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
ref = emb(src, de, ate, "ref")
res = []
for d in sorted(L.glob("ad*")):
    for f in ("narr_fim.mp3", "narr_fim_univ.mp3"):
        p = d / f
        if p.exists():
            v = (d / "voz.txt").read_text().strip() if (d / "voz.txt").exists() else "?"
            res.append((float(np.dot(ref, emb(p, n=d.name))), d.name, v)); break
for r in sorted(res, reverse=True): print("%.3f %s %s" % r)

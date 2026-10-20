# -*- coding: utf-8 -*-
import subprocess, tempfile, sys
from pathlib import Path
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
L = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho")
B = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM")
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de=None, ate=None, nome="x"):
    o = tmp / f"{nome}.wav"; c = ["-ss", str(de), "-to", str(ate)] if de is not None else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *c, "-i", str(src), "-ac", "1", "-ar", "16000", str(o)], check=True)
    return enc.embed_utterance(preprocess_wav(o))
alvos = {n: emb(B / "originais" / f"{n}.mp4", float(de), float(ate), "o" + n) for n, de, ate in (x.split(":") for x in sys.argv[1:])}
for d in sorted(L.glob("ad*")):
    v = d / "voz.txt"; f = d / "narr_fim.mp3"
    if not f.exists(): continue
    vid = v.read_text(encoding="utf-8-sig").strip() if v.exists() else "?"
    g = emb(f, nome=d.name)
    print(d.name, vid, " ".join(f"{n}={float(np.dot(e, g)):.3f}" for n, e in alvos.items()))

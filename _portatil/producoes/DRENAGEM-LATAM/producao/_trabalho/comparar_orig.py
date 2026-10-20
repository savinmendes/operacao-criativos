import subprocess, tempfile
from pathlib import Path
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
S = Path(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20"); B = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM")
enc = VoiceEncoder(verbose=False); tmp = Path(tempfile.mkdtemp())
def emb(src, de, ate, n):
    o = tmp / f"{n}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(de), "-to", str(ate), "-i", str(src), "-ac", "1", "-ar", "16000", str(o)], check=True)
    return enc.embed_utterance(preprocess_wav(o))
a30 = emb(B/"originais"/"30.mp4", 18, 120, "a"); b30 = emb(B/"originais"/"30.mp4", 150, 300, "b")
a18 = emb(B/"originais"/"18.mp4", 4, 58, "c")
print("30 self", float(np.dot(a30, b30)))
for f in sorted(S.glob("AD *.mp4")):
    try: e = emb(f, 10, 60, f.stem.replace(" ", ""))
    except Exception as x: continue
    print(f.stem, f"30={float(np.dot(a30, e)):.3f} 18={float(np.dot(a18, e)):.3f}")

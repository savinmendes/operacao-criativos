import numpy as np, librosa
from faster_whisper import WhisperModel
def mf(p, a=None, b=None):
    y, sr = librosa.load(p, sr=16000)
    if a is not None: y = y[int(a*sr):int(b*sr)]
    y, _ = librosa.effects.trim(y, top_db=35)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, hop_length=160)[1:]
    return (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)
ref = mf("gancho.wav", 0.0, 2.65)
w = WhisperModel("medium", device="cpu", compute_type="int8")
for n in ["ab_stock", "ab_estoque"]:
    x = mf(f"_teste/{n}.mp3")
    D, wp = librosa.sequence.dtw(ref, x, metric="euclidean")
    s, _ = w.transcribe(f"_teste/{n}.mp3", language="es")
    print(n, "dtw_norm=%.3f" % (D[-1, -1] / len(wp)), "| whisper:", " ".join(t.text for t in s))

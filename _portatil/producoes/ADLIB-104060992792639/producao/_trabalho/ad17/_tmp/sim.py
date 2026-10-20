import sys, numpy as np, librosa, warnings; warnings.filterwarnings("ignore")
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder("cpu")
def emb(p, a=None, b=None):
    y, sr = librosa.load(p, sr=16000, mono=True, offset=a or 0, duration=(b - a) if b else None)
    return enc.embed_utterance(preprocess_wav(y, 16000))
def f0(p, a=None, b=None):
    y, sr = librosa.load(p, sr=16000, mono=True, offset=a or 0, duration=(b - a) if b else None)
    f, v, _ = librosa.pyin(y, fmin=70, fmax=500, sr=16000); return np.nanmedian(f)
refs = {"ORACAO-11 mulher": ("ad11/_audio/clone_mulher.wav", None, None),
        "ORACAO-13 mulher": ("ad13/_audio/demucs/htdemucs/orig/vocals.wav", 7, 120),
        "ORACAO-11 menina": ("ad11/_audio/clone_menina.wav", None, None),
        "ORACAO-05 Clara": ("ad05/_audio/demucs/htdemucs/orig/vocals.wav", 0, 3)}
alvos = [tuple(x.split(":")) for x in sys.argv[1:]]  # nome:arquivo:a:b
E = {k: emb(*v) for k, v in refs.items()}
for nome, p, a, b in alvos:
    e = emb(p, float(a), float(b))
    print(nome, f"f0={f0(p, float(a), float(b)):.0f}Hz", " | ".join(f"{k}={float(np.dot(e, v)):.3f}" for k, v in E.items()))
for k, v in refs.items(): print("ref", k, f"f0={f0(*v):.0f}Hz")

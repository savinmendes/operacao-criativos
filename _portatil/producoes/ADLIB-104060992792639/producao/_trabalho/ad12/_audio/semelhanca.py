import numpy as np, librosa, warnings; warnings.filterwarnings("ignore")
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder(verbose=False)
def emb(p, t0=None, t1=None):
    y, sr = librosa.load(p, sr=16000, offset=t0 or 0, duration=(t1 - t0) if t1 else None)
    return enc.embed_utterance(preprocess_wav(y, 16000))
def f0(p,t0=0,t1=None):
    y, sr = librosa.load(p, sr=16000, offset=t0, duration=(t1-t0) if t1 else None)
    f,v,_ = librosa.pyin(y, fmin=80, fmax=400, sr=sr); return np.nanmedian(f)
R = {"12 corpo": ("ad12/_audio/demucs/htdemucs/orig/vocals.wav", 10, 106),
     "12 gancho": ("ad12/_audio/demucs/htdemucs/orig/vocals.wav", 0, 9.5),
     "14 gancho": ("ad14/_audio/demucs/htdemucs/hook/vocals.wav", 0, 9.4),
     "fonte clone 11 mulher": ("ad11/_audio/clone_mulher.wav", None, None),
     "01 voz orig": ("ad01/_audio/demucs/htdemucs/orig/vocals.wav", 0, 110),
     "13 voz orig": ("ad13/_audio/demucs/htdemucs/orig/vocals.wav", 7, 118),
     "TTS clone 11 mulher (ad01 b4)": ("ad01/_audio/tts/b4.mp3", None, None),
     "TTS clone 13 mulher (ad13 b4)": ("ad13/_audio/tts/b4.mp3", None, None)}
E = {k: emb(*v) for k, v in R.items()}
ks = list(R)
for a in ks[:3]:
    print(a, " | ".join(f"{b}: {float(E[a] @ E[b]):.3f}" for b in ks if b != a))
for k,v in R.items():
    print(k, "F0", round(float(f0(v[0], v[1] or 0, v[2])),1))

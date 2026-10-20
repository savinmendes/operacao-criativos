from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np, sys, librosa
enc=VoiceEncoder(verbose=False)
W="C:/Users/PICHAU/Downloads/ADLIB-104060992792639/producao/_trabalho/"
fs={"ad16":W+"ad16/_audio/demucs/htdemucs/orig/vocals.wav",
    "ad11_mulher":W+"ad11/_audio/clone_mulher.wav","ad11_tts":W+"ad11/_audio/tts/b1.mp3",
    "ad05_desat":W+"ad05/_audio/clone_desatadora.wav","ad13_mulher":W+"ad13/_audio/demucs/htdemucs/orig/vocals.wav",
    "ad13_tts":W+"ad13/_audio/tts/b2.mp3","ad11_menina":W+"ad11/_audio/clone_menina.wav"}
E={}
for k,v in fs.items():
    y,sr=librosa.load(v,sr=16000); E[k]=enc.embed_utterance(preprocess_wav(y,source_sr=16000))
    f0=librosa.yin(y,fmin=80,fmax=400,sr=16000); print(k,"f0 med",round(float(np.median(f0)),0))
ks=list(E)
print("            "+" ".join(f"{k[:10]:>11}" for k in ks))
for a in ks: print(f"{a[:11]:>11} "+" ".join(f"{float(E[a]@E[b]):11.3f}" for b in ks))

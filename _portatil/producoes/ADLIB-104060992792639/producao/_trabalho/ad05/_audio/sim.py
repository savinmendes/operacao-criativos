from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np, sys
enc=VoiceEncoder(verbose=False)
fs={"clara":"clone_clara.wav","homem":"clone_homem.wav","desat":"clone_desatadora.wav",
    "ad11_mulher":"../../ad11/_audio/clone_mulher.wav","ad11_menina":"../../ad11/_audio/clone_menina.wav"}
E={k:enc.embed_utterance(preprocess_wav(v)) for k,v in fs.items()}
ks=list(E)
print("        "+" ".join(f"{k[:9]:>10}" for k in ks))
for a in ks: print(f"{a[:9]:>9} "+" ".join(f"{float(E[a]@E[b]):10.3f}" for b in ks))

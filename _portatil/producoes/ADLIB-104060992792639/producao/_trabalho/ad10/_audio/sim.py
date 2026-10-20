from resemblyzer import VoiceEncoder, preprocess_wav
import sys
enc=VoiceEncoder(verbose=False)
fs={"hosp10":"v_hosp.wav","desat10":"v_desat.wav","desat09":"../../ad09/_audio/v_desat.wav","ad11_mulher":"../../ad11/_audio/clone_mulher.wav",
    "ad05_desat":"../../ad05/_audio/clone_desatadora.wav","ad13_mulher":"ad13_mulher.wav","ad11_menina":"../../ad11/_audio/clone_menina.wav"}
for a in sys.argv[1:]: k,v=a.split("="); fs[k]=v
E={k:enc.embed_utterance(preprocess_wav(v)) for k,v in fs.items()}
ks=list(E)
print("          "+" ".join(f"{k[:10]:>11}" for k in ks))
for a in ks: print(f"{a[:10]:>10} "+" ".join(f"{float(E[a]@E[b]):11.3f}" for b in ks))

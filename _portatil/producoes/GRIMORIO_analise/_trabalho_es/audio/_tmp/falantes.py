import os, sys, json
os.add_dll_directory(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib")
os.environ["PATH"] = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_vg\Lib\site-packages\torch\lib;" + os.environ["PATH"]
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa, numpy as np
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
segs, _ = m.transcribe("vocals.wav", language="pt", word_timestamps=True)
ws=[]; S=[]
for s in segs:
    S.append((s.start,s.end,s.text))
    for w in s.words: ws.append((round(w.start,3),round(w.end,3),w.word))
json.dump(ws, open("pt_palavras.json","w",encoding="utf-8"), ensure_ascii=False)
y, sr = librosa.load("vocals.wav", sr=16000)
enc = VoiceEncoder(verbose=False)
ref = enc.embed_utterance(preprocess_wav(y[100*sr:125*sr], source_sr=sr))
for a,b,t in S:
    seg = y[int(a*sr):int(b*sr)]
    e = enc.embed_utterance(preprocess_wav(seg, source_sr=sr))
    f0,_,_ = librosa.pyin(seg, fmin=60, fmax=400, sr=sr)
    print(f"{a:6.2f}-{b:6.2f} sim_roxo={float(e@ref):.2f} f0={np.nanmedian(f0):5.0f} |{t}")

from resemblyzer import VoiceEncoder, preprocess_wav
import librosa, numpy as np
y, sr = librosa.load("vocals.wav", sr=16000); enc=VoiceEncoder(verbose=False)
E=lambda a,b: enc.embed_utterance(preprocess_wav(y[int(a*sr):int(b*sr)], source_sr=sr))
s={'mulher':E(0,3.86),'grito':E(4.12,6.84),'chora':E(7.38,21.7),'roxo':E(30,60)}
for a in s:
  print(a, {b: round(float(s[a]@s[b]),2) for b in s})

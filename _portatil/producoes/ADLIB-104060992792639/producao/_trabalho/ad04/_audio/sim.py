import sys, numpy as np, librosa
from resemblyzer import VoiceEncoder, preprocess_wav
enc=VoiceEncoder(verbose=False)
def emb(f,a=None,b=None):
    y,sr=librosa.load(f,sr=16000,offset=a or 0,duration=(b-a) if b else None)
    return enc.embed_utterance(preprocess_wav(y,16000))
def pitch(f,a=None,b=None):
    y,sr=librosa.load(f,sr=16000,offset=a or 0,duration=(b-a) if b else None)
    f0,v,_=librosa.pyin(y,fmin=70,fmax=500,sr=sr); return np.nanmedian(f0)
refs={'11 mulher':('ad11/_audio/clone_mulher.wav',None,None),'11 menina':('ad11/_audio/clone_menina.wav',None,None),
 '13 mulher':('ad13/_audio/demucs/htdemucs/orig/vocals.wav',7,120),'05 clara':('ad05/_audio/demucs/htdemucs/orig/vocals.wav',12,27)}
alvos=[(x.split('|')[0],x.split('|')[1],float(x.split('|')[2]),float(x.split('|')[3])) for x in sys.argv[1:]]
R={k:emb(*v) for k,v in refs.items()}
for k,v in refs.items(): print('ref',k,'pitch',round(float(pitch(*v)),0))
for nome,f,a,b in alvos:
    e=emb(f,a,b); print(nome,'pitch',round(float(pitch(f,a,b)),0),{k:round(float(np.dot(e,r)),3) for k,r in R.items()})

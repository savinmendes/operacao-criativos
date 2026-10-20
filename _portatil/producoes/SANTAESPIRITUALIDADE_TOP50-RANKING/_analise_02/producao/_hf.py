import sys, glob, os, librosa, numpy as np
from scipy.signal import stft
def hf(p,sr=44100):
    x,_=librosa.load(p,sr=sr,mono=True); f,t,Z=stft(x,sr,nperseg=4096); P=np.abs(Z)**2
    r=P[(f>7000)&(f<16000)].mean(0)/(P[f>100].mean(0)+1e-12)
    e=P.sum(0); q=np.percentile(e,15); fl=P[(f>7000)][:, e<=q].mean()
    return round(float(10*np.log10(np.median(r)+1e-12)),1), round(float(10*np.log10(fl+1e-15)),1), round(float(np.abs(x).max()),3)
for p in sys.argv[1:]: print(os.path.basename(p), "HF/tot, piso HF, pico:", hf(p))

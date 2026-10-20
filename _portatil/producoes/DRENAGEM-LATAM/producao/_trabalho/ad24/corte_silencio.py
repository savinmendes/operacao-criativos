import numpy as np, soundfile as sf, sys
y,sr=sf.read("aud/voc16.wav")
def melhor(t,w=0.35):
    a=int((t-w)*sr); b=int((t+w)*sr); f=int(0.03*sr); h=int(0.01*sr)
    best=None
    for i in range(a,b-f,h):
        e=np.sqrt(np.mean(y[i:i+f]**2))
        if best is None or e<best[0]: best=(e,i)
    return round((best[1]+f/2)/sr,3), round(20*np.log10(best[0]+1e-9),1)
for t in map(float,sys.argv[1:]): print(t, *melhor(t))

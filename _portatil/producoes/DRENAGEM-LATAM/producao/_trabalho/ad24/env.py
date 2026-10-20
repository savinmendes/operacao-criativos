import numpy as np, soundfile as sf, sys
y,sr=sf.read("aud/voc16.wav")
for t in map(float,sys.argv[1:]):
    s=[]
    for k in range(-15,16):
        c=t+k*0.03; i=int(c*sr); f=int(0.03*sr)
        s.append(int(20*np.log10(np.sqrt(np.mean(y[i:i+f]**2))+1e-9)))
    print(t, " ".join(f"{v}" for v in s))

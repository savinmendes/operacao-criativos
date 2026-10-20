import numpy as np, soundfile as sf
from scipy.signal import welch
def band(x,sr,a,b,lo,hi):
    s=x[int(a*sr):int(b*sr)]
    if len(s)<2048: return np.nan
    f,p=welch(s,sr,nperseg=2048); m=(f>=lo)&(f<hi)
    return 10*np.log10(p[m].mean()+1e-20)
A={k:sf.read(f'a_{k}.wav') for k in ('v3','v1')}
pauses=[(4.95,5.25),(8.3,10.7),(12.6,13.05),(14.75,15.15),(21.62,22.1),(33.4,33.7),(36.72,37.25),(42.85,43.25),(50.1,50.65),(60.6,61.25)]
print('pausa        v3 7-14k  v1 7-14k | v3 2-5k v1 2-5k')
for a,b in pauses:
    r=[band(A[k][0],A[k][1],a,b,7000,14000) for k in ('v3','v1')]+[band(A[k][0],A[k][1],a,b,2000,5000) for k in ('v3','v1')]
    print(f'{a:5.2f}-{b:5.2f}  '+'  '.join(f'{v:7.1f}' for v in r))
for k in ('v3','v1'):
    x,sr=A[k]
    print(k,'fala inteira 7-14k',round(band(x,sr,0,61,7000,14000),1),'14-20k',round(band(x,sr,0,61,14000,20000),1),'0.1-1k',round(band(x,sr,0,61,100,1000),1))

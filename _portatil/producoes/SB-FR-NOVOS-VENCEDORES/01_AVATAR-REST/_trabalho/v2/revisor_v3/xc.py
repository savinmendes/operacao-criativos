import numpy as np, soundfile as sf
x,sr=sf.read('../voz_v3.wav'); x=x.mean(1) if x.ndim>1 else x
lines=open('boca.txt').read().split('\n')
segs={}
for i,l in enumerate(lines):
    if l.startswith('P '): k=int(l[2:]); segs[k]=[(float(a),float(b)) for a,b in (t.split(':') for t in lines[i+1].split())]
for k,v in segs.items():
    t=np.array([a for a,b in v]); m=np.array([b for a,b in v]); ok=~np.isnan(m)
    e=np.array([np.sqrt(np.mean(x[int((ti-0.02)*sr):int((ti+0.0533)*sr)]**2)) for ti in t])
    e=20*np.log10(e+1e-6)
    res=[]
    for lag in range(-9,10):
        # mouth at t vs audio at t+lag
        ee=np.array([20*np.log10(np.sqrt(np.mean(x[int((ti+lag/30-0.02)*sr):int((ti+lag/30+0.0533)*sr)]**2))+1e-6) for ti in t])
        c=np.corrcoef(m[ok],ee[ok])[0,1]; res.append((lag*33,round(c,2)))
    best=max(res,key=lambda r:r[1]); print(k,'best lag ms (audio later than mouth if +)',best, res[6:13])

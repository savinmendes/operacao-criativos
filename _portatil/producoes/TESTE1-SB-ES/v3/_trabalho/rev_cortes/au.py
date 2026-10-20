import numpy as np,soundfile as sf,json
a,sr=sf.read('a48.wav');m=a.mean(1)
# rms 100ms
h=int(.1*sr);n=len(m)//h
r=20*np.log10(np.sqrt((m[:n*h].reshape(n,h)**2).mean(1))+1e-9)
np.save('rms.npy',r)
# low windows (pauses) in padre section 55-169: 10th percentile per 5s
for t in range(55,169,5):
    seg=r[t*10:(t+5)*10]; print(t, 'min',round(seg.min(),1),'p10',round(np.percentile(seg,10),1),'max',round(seg.max(),1))
# clicks: second-diff spikes
d=np.abs(np.diff(m,2)); th=np.percentile(d,99.99)
idx=np.where(d>max(th,0.15))[0]
print('click cand',len(idx),[round(i/sr,3) for i in idx[:40]])

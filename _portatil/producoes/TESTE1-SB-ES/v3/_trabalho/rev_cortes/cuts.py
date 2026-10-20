import numpy as np
a=np.load('fr.npy').astype(np.float32)
# mask out overlays? use central region rows 30..200 (exclude top selo & bottom)
g=a.mean(3)
d=np.abs(np.diff(g,axis=0)).mean((1,2))
lum=g.mean((1,2))
np.save('d.npy',d);np.save('lum.npy',lum)
med=np.median(d)
cuts=[]
for i in range(len(d)):
    lo=max(0,i-5);hi=min(len(d),i+6)
    loc=np.median(np.r_[d[lo:i],d[i+1:hi]])
    if d[i]>12 and d[i]>3*loc+4: cuts.append(i+1)
print(len(cuts))
for c in cuts: print(c, round(c/30,3), round(float(d[c-1]),1), 'lum', round(float(lum[c-1]),1), round(float(lum[c]),1))
print('dark frames', [ (i,round(i/30,2)) for i in np.where(lum<12)[0]])

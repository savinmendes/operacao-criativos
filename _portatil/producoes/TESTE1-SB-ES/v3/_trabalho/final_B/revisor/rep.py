import json,collections,numpy as np,os
d=json.load(open(r'C:/Users/PICHAU/Downloads/TESTE1-SB-ES/v3/_trabalho/final_B/timeline_B.json',encoding='utf-8'))
P=d['planos'];c=collections.defaultdict(list)
B=lambda p: os.path.basename(p['file'].replace(chr(92),'/'))
for p in P: c[B(p)].append((round(p['t0'],2),p.get('vt'),p['n']))
for k,v in c.items():
    if len(v)>1: print(k,v)
a=np.load('gray.npy',mmap_mode='r')
mids=[(p['q0']+p['n']//2,B(p)) for p in P]
for i in range(len(mids)):
    for j in range(i+1,len(mids)):
        if mids[i][1]!=mids[j][1]:
            dd=np.abs(a[mids[i][0]].astype(float)-a[mids[j][0]]).mean()
            if dd<12: print('parecido',mids[i],mids[j],round(dd,1))

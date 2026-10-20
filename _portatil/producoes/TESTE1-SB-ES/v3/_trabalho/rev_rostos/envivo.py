import json
from PIL import Image
import numpy as np
d=json.load(open('../final/timeline_v3.json',encoding='utf-8'))
def has(q):
    a=np.asarray(Image.open('f/%05d.jpg'%(q+1)).crop((405,65,515,108))).astype(int)
    pink=(a[...,0]>200)&(a[...,1]<80)&(a[...,2]>90)&(a[...,2]<180)
    return pink.mean()
res={}
for q in range(5085): res[q]=has(q)
# frames by plano
for p in d['planos']:
    q0,n=p['q0'],p['n']; vals=[res[q] for q in range(q0,min(q0+n,5085))]
    on=sum(v>0.3 for v in vals)
    print('%7.2f-%7.2f %-30s live=%s envivo %d/%d'%(p['t0'],p['t1'],p.get('broll') or p['item'],p.get('live'),on,len(vals)))

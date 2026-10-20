import numpy as np
from PIL import Image
def ycount(i,y0,y1):
    a=np.asarray(Image.open(f"f/{i+1:05d}.jpg").crop((0,y0,720,y1))).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    return int(((r>200)&(g>190)&(b<90)).sum())
import sys
res={}
for name,(y0,y1) in {"giant":(700,880),"cta":(1040,1160)}.items():
    prev=False; segs=[]
    for i in range(4299):
        on=ycount(i,y0,y1)>1500
        if on and not prev: st=i
        if prev and not on: segs.append((st,i-1))
        prev=on
    if prev: segs.append((st,4298))
    print(name,[(a,b,round(a/30,2),round((b+1)/30,2)) for a,b in segs if b-a>3])

import numpy as np,cv2
a=np.load('fr.npy');d=np.load('d.npy');N=len(a)
cuts=[285, 375, 465, 555, 643, 668, 816, 830, 1044, 1075, 1188, 1228, 1317, 1378, 1620, 1644, 1649, 1759, 1794, 1825, 1896, 1925, 1998, 2026, 2076, 2132, 2171, 2256, 2298, 2378, 2420, 2697, 2761, 2791, 2862, 2925, 2960, 3027, 3090, 3171, 3287, 3328, 3368, 3435, 3495, 3529, 3605, 3695, 3809, 3846, 3904, 3975, 4046, 4074, 4107, 4242, 4322, 4366, 4427, 4500, 4576, 4666, 4724, 4764, 4833, 4885, 4922, 4970]
b=[0]+cuts+[N]
shots=[(b[i],b[i+1]) for i in range(len(b)-1)]
def feat(f):
    g=cv2.cvtColor(f,cv2.COLOR_RGB2GRAY)[20:170].astype(np.float32)
    g=cv2.resize(g,(32,40),interpolation=cv2.INTER_AREA)
    g=(g-g.mean())/(g.std()+1e-6);return g.ravel()
F=[]
for s,e in shots:
    idx=np.linspace(s,e-1,min(5,e-s)).astype(int)
    F.append(np.array([feat(a[i]) for i in idx]))
res=[]
for i in range(len(shots)):
    for j in range(i+1,len(shots)):
        if j==i+1: continue
        c=max(float((x@y)/len(x)) for x in F[i] for y in F[j])
        # also mirrored
        res.append((c,i,j))
res.sort(reverse=True)
for c,i,j in res[:25]:
    print(round(c,3),i,shots[i],round(shots[i][0]/30,2),'<->',j,shots[j],round(shots[j][0]/30,2))
import json
t=json.load(open('../final/timeline_v3.json',encoding='utf8'))['itens']
def lab(s,e):
    m=(s+e)/2/30
    for it in t:
        if it['V0']<=m<it['V1']: return it['id'],it['tipo']
    return '?','?'
L=[lab(*s) for s in shots]
print('\n--- shots')
for i,(s,e) in enumerate(shots): print(i,round(s/30,2),round(e/30,2),e-s,L[i])
print('\n--- pares com b-roll (nao take x take)')
for c,i,j in res:
    if c<0.80: break
    if L[i][1]=='take' and L[j][1]=='take' and L[i][0] not in ('P06',) : continue
    print(round(c,3),i,round(shots[i][0]/30,2),L[i],'<->',j,round(shots[j][0]/30,2),L[j])

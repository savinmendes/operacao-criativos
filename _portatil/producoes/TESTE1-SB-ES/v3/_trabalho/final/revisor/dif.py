import cv2,numpy as np,json
N=5085
prev=None;d=[0.0];lum=[]
for i in range(N):
    im=cv2.imread(f'f/{i:05d}.jpg',0); s=cv2.resize(im,(90,160)).astype(np.float32)
    lum.append(float(s.mean()))
    if prev is not None: d.append(float(np.abs(s-prev).mean()))
    prev=s
np.save('dif.npy',np.array(d)); np.save('lum.npy',np.array(lum))
tl=json.load(open('../timeline_v3.json',encoding='utf-8'))
cuts=[p['q0'] for p in tl['planos']][1:]
d=np.array(d)
# detected cuts: diff > max(12, 3*median of neighbors)
det=[i for i in range(1,N) if d[i]>10 and d[i]>3*np.median(d[max(1,i-5):i+6])]
print('planned',len(cuts)); print('detected',len(det),det)
print('planned not detected (+-2):',[c for c in cuts if not any(abs(c-x)<=2 for x in det)])
print('detected not planned:',[x for x in det if not any(abs(c-x)<=2 for c in cuts)])
print('dark frames',[i for i,l in enumerate(lum) if l<15])

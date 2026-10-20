import numpy as np,soundfile as sf,json
r=np.load('rms.npy')
low=np.where(r[550:]<-42)[0]+550
# group
g=[];
for i in low:
    if g and i-g[-1][1]<=1: g[-1][1]=i
    else: g.append([i,i])
print('janelas < -42 dBFS (padre):',[(round(a/10,1),round((b+1)/10,1),round(r[a:b+1].min(),1)) for a,b in g])
a,sr=sf.read('a48.wav');m=a.mean(1)
d=np.abs(np.diff(m,2));
t=json.load(open('../final/timeline_v3.json',encoding='utf8'))
for it in t['itens']:
    for b in (it['T0'],it['T0']+(it['uso'][1]-it['uso'][0])):
        s=max(int(b*sr),sr); w=d[s-int(.03*sr):s+int(.03*sr)]; bg=np.median(d[s-sr//2:s+sr//2])
        print(it['id'],round(b,3),'pico2diff',round(w.max(),3),'mediana',round(bg,4), 'rms',round(r[int(b*10)],1))

import numpy as np, subprocess, json
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32)
hg=load('padre_hg_720.mp4'); v=load('voz_v3.wav'); sr=16000
mp=json.load(open('mapa_padre.json')); segs={}
for f,s,h in mp: segs.setdefault(s,[]).append((f,h))
for s,l in segs.items():
    for k in (0,len(l)//2,len(l)-25):
        f0,h0=l[k]; t_final=f0/30; t_hg=h0/25
        a=hg[int(t_hg*sr):int((t_hg+0.8)*sr)]
        best=(0,-1)
        for lag_ms in range(-1500,1501,5):
            st=int((t_final+lag_ms/1000)*sr); b=v[st:st+len(a)]
            if len(b)<len(a): continue
            c=np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)+1e-9)
            if c>best[1]: best=(lag_ms,c)
        print(s,'frame',f0,'t=%.2f'%t_final,'lag %+d ms corr %.2f rms_hg %.3f'%(best[0],best[1],np.sqrt(np.mean(a**2))))

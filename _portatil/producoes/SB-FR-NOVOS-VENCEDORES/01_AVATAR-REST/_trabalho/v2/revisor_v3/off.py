import numpy as np, soundfile as sf, subprocess, json
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32)
hg=load('padre_hg_720.mp4'); v=load('voz_v3.wav'); sr=16000
mp=json.load(open('mapa_padre.json'))
# per seg: first final frame f, hg frame h (25fps assumed?)
segs={}
for f,s,h in mp: segs.setdefault(s,[]).append((f,h))
for s,l in segs.items():
    f0,h0=l[0]; f1,h1=l[-1]
    fps_hg=(h1-h0)/((f1-f0)/30)
    print(s,'hg fps est',round(fps_hg,2))
    t_final=f0/30; t_hg=h0/25
    # take hg audio window t_hg..t_hg+2 and find in v around t_final
    a=hg[int(t_hg*sr):int((t_hg+2)*sr)]
    best=None
    for lag_ms in range(-400,401,5):
        st=int((t_final+lag_ms/1000)*sr); b=v[st:st+len(a)]
        c=np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)+1e-9)
        if best is None or c>best[1]: best=(lag_ms,c)
    print('  audio do HG em t_hg aparece na voz final em t_final%+d ms (corr %.2f)'%(best[0],best[1]))

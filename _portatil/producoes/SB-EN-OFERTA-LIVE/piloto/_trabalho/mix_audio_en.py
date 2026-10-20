import soundfile as sf, numpy as np, subprocess, json
SR=48000; TOTAL=23.87; HK=3.2
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
voz=load("audio/voz_en.wav")
bed=load("demucs/es_no_vocals.wav")
ES=[0,3.23,7.40,8.85,12.55,16.40,19.35,22.53,25.85,30.27]
FR=json.load(open("cortes_en.json"))  # 10 fronteiras
out=np.zeros_like(voz); fade=int(0.05*SR)
for k in range(9):
    L=FR[k+1]-FR[k]; es_end=ES[k+1]
    a=int((es_end-L)*SR); n=int(L*SR)
    seg=np.zeros((n+fade,2),np.float32)
    src=bed[max(0,a):max(0,a)+n+fade]
    off=max(0,-a); seg[off:off+len(src)]=src[:n+fade-off]
    env=np.ones(n+fade,np.float32); env[:fade]=np.linspace(0,1,fade); env[-fade:]=np.linspace(1,0,fade)
    s=int(FR[k]*SR); e=min(len(out),s+n+fade)
    if k==0: env[:fade]=1
    out[s:e]+=(seg*env[:,None])[:e-s]
sf.write("audio/trilha_en.wav",out,SR)

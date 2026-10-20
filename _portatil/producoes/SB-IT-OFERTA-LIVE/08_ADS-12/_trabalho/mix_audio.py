import soundfile as sf, numpy as np, subprocess, json, pyloudnorm as pyln
SR=48000; CJ=json.load(open("cortes_en.json")); C,ES=CJ["C"],CJ["ES"]
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
voz=load("audio/voz_en.wav"); bed=load("demucs/htdemucs/es_audio/no_vocals.wav")
out=np.zeros_like(voz); fade=int(0.05*SR)
for k in range(6):
    n=int((C[k+1]-C[k])*SR); a=int(ES[k]*SR)
    seg=np.zeros((n+fade,2),np.float32); src=bed[a:a+n+fade]; seg[:len(src)]=src
    env=np.ones(n+fade,np.float32); env[-fade:]=np.linspace(1,0,fade)
    if k>0: env[:fade]=np.linspace(0,1,fade)
    s=int(C[k]*SR); e=min(len(out),s+n+fade); out[s:e]+=(seg*env[:,None])[:e-s]
m=pyln.Meter(SR)
lv=m.integrated_loudness(voz); voz=voz*10**((-16-lv)/20)
lb=m.integrated_loudness(out); out=out*10**((-32-lb)/20)
print("voz",round(lv,1),"bed",round(lb,1))
mix=voz+out; pk=np.abs(mix).max()
if pk>0.95: mix*=0.95/pk
sf.write("audio/mix_en.wav",mix,SR); print("ok",len(mix)/SR)

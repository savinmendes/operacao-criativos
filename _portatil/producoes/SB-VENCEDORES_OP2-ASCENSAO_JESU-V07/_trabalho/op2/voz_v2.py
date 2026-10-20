import soundfile as sf, numpy as np, subprocess
SR=48000; HK=3.30; TOTAL=27.40
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
h=load("audio/hook_fr.wav"); c=load("audio/corpo_fr_v2.wav")
v=np.zeros((int(TOTAL*SR),2),np.float32); m=min(len(h),int(HK*SR)); v[:m]=h[:m]
i=int(HK*SR); n=min(len(c),len(v)-i); v[i:i+n]=c[:n]
sf.write("audio/voz_fr_v2.wav",v,SR)
for nome,a,b in [("clipA",17.30,20.60),("clipB",23.05,27.40)]:
    sf.write(f"audio/{nome}.wav",v[int(a*SR):int(b*SR)],SR)

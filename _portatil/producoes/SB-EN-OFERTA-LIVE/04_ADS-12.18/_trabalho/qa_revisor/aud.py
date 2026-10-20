import subprocess, numpy as np
def rd(p):
    b=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32)
F=rd(r"..\SB-EN-ADS-12.18.mp4"); Vo=rd(r"audio\voz_en.wav"); M=rd(r"demucs\htdemucs\es\no_vocals.wav"); E=rd(r"demucs\htdemucs\es\vocals.wav")
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
w=1600
print("len s",len(F)/16000,len(Vo)/16000,len(M)/16000,len(E)/16000)
for i in range(0,int(len(F)/w)):
    s=slice(i*w,(i+1)*w)
    def g(a): return db(a[s]) if len(a)>=(i+1)*w else -99
    print(f"{i*0.1:5.1f} final {g(F):6.1f} vozEN {g(Vo):6.1f} musica {g(M):6.1f} vozES {g(E):6.1f}")

# Áudio v2 sem chiado: cada mp3 de voz limpo (afftdn com perfil das pausas + lowpass) -> montado na timeline FR (igual timeline.py)
# -> gate suave nas pausas (pelas palavras) -> ganho linear por personagem (-14 LUFS) + limiter -> jump cuts -> trilha limpa -32 LUFS.
import json,subprocess,numpy as np,soundfile as sf,sys
sys.path.insert(0,'..'); from palavras import palavras
import pyloudnorm as pyln
SR=48000; TOTAL=62.3
def ff(inp,af,out): subprocess.run(["ffmpeg","-v","error","-y","-i",inp,"-af",af,"-ar",str(SR),"-ac","2",out],check=True)
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
# 1) limpeza por arquivo: perfil de ruído aprendido nas pausas (asendcmd liga o "sample noise" nos trechos sem fala)
LP={"temo":10500,"hook":10500,"padre":11000}
for nm in ["hook","temo","padre"]:
    W=palavras(f"../audio/{nm}_fr.alinhamento.json"); P=[]; prev=0
    for w,s,e in W:
        if s-prev>0.3: P.append((prev+0.06,s-0.06))
        prev=e
    cmd=";".join(f"{a:.3f} afftdn@n sn start; {b:.3f} afftdn@n sn stop" for a,b in P[:3])
    af=f"highpass=f=70,asendcmd=c='{cmd}',afftdn@n=nr=14:nf=-60:tn=1,lowpass=f={LP[nm]}:p=2,lowpass=f={LP[nm]+1500}:p=2,deesser=i=0.25"
    ff(f"../audio/{nm}_fr.mp3",af,f"limpo_{nm}.wav"); print(nm,"pausas perfil",P[:3])
FALAS=[("hook",0.04,4.16,0.09,"comerciante"),("hook",4.76,7.70,5.20,"comerciante"),("temo",0.04,17.83,10.84,"comerciante"),
 ("padre",0.08,3.47,29.10,"padre"),("padre",4.08,5.26,33.00,"padre"),("padre",5.77,8.89,34.70,"padre"),
 ("padre",9.50,15.15,38.25,"padre"),("padre",15.76,18.55,44.25,"padre"),("padre",19.25,22.85,47.60,"padre"),
 ("padre",23.66,28.22,51.60,"padre"),("padre",28.92,33.99,56.60,"padre")]
vozes={"comerciante":np.zeros((int(TOTAL*SR),2),np.float32),"padre":np.zeros((int(TOTAL*SR),2),np.float32)}
env={k:np.zeros(int(TOTAL*SR),np.float32) for k in vozes}
cache={}
for arq,i0,i1,ab,per in FALAS:
    if arq not in cache: cache[arq]=(load(f"limpo_{arq}.wav"),palavras(f"../audio/{arq}_fr.alinhamento.json"))
    au,pw=cache[arq]; off=ab-i0; a0=max(0,i0-0.06); a1=i1+0.15
    seg=au[int(a0*SR):int(a1*SR)].copy(); n=len(seg); f=int(0.01*SR); seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    p=int((a0+off)*SR); vozes[per][p:p+n]+=seg[:len(vozes[per])-p]
    for w,s,e in pw:
        if s>=i0-0.01 and e<=i1+0.01:
            env[per][max(0,int((s+off-0.07)*SR)):int((e+off+0.10)*SR)]=1
# 2) gate suave nas pausas: -30 dB fora das palavras, rampas de 40 ms
k=int(0.04*SR); ker=np.ones(k)/k; meter=pyln.Meter(SR); out=np.zeros((int(TOTAL*SR),2),np.float32)
for per,v in vozes.items():
    g=np.convolve(np.maximum(env[per],10**(-30/20)),ker,"same").astype(np.float32); v=v*g[:,None]
    act=v[env[per]>0.5]; L=meter.integrated_loudness(act); gain=10**((-16-L)/20); print(per,"LUFS fala %.1f ganho %+.1f dB"%(L,20*np.log10(gain)))
    out+=v*gain
sf.write("voz_limpa.wav",out,SR,subtype="FLOAT"); print("pico voz",np.abs(out).max())
# limiter + jump cuts (mesmos quadros do final.sh)
A1,B1,A2,B2=386/30,402/30,465/30,479/30; TOT=round(62.3-30/30,3)
ff("voz_limpa.wav",f"alimiter=limit=0.85:attack=3:release=60:level=disabled,aselect='not(between(t,{A1},{B1}-0.00001)+between(t,{A2},{B2}-0.00001))',asetpts=N/SR/TB","voz_cut.wav")
# 3) trilha: demucs sem voz, denoise + lowpass 11,5 kHz, -32 LUFS
ff("../demucs/htdemucs/es/no_vocals.wav",f"atrim=0:{TOT},afftdn=nr=12:nf=-55:tn=1,lowpass=f=11500:p=2,afade=t=in:d=0.05,afade=t=out:st={TOT-0.8}:d=0.8","trilha_tmp.wav")
t,_=sf.read("trilha_tmp.wav"); Lt=meter.integrated_loudness(t); t=t*10**((-32-Lt)/20); sf.write("trilha_cut.wav",t.astype(np.float32),SR,subtype="FLOAT")
v,_=sf.read("voz_cut.wav"); n=max(len(v),len(t)); m=np.zeros((n,2)); m[:len(v)]+=v; m[:len(t)]+=t; m=m[:int(TOT*SR)]
print("trilha %.1f -> -32; pico mix %.2f; mix LUFS %.1f"%(Lt,np.abs(m).max(),meter.integrated_loudness(m)))
sf.write("mix_v2.wav",np.clip(m,-0.98,0.98).astype(np.float32),SR,subtype="FLOAT")

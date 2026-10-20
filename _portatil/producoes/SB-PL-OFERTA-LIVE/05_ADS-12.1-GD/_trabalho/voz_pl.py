# Voz PL na linha do tempo original (cortes de cena do ES mantidos). Gera audio/voz_pl.wav, palavras_pl.json e mp3 por trecho de lipsync
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; TOTAL=31.60
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
A={n:(load(f"audio/{n}.mp3"),palavras(f"audio/{n}.alinhamento.json")) for n in ["hook_pl","b_pl","corpo_pl","cta1_pl","cta2_pl"]}
P=[("hook_pl",0.0,4.83,0.20),
   ("b_pl",0.0,3.81,5.75),
   ("corpo_pl",0.0,1.25,10.10),    # Jezus cię wybrał.
   ("corpo_pl",1.30,3.20,11.80),   # Przyniósł ci potężny dar.
   ("corpo_pl",3.30,6.27,14.35),   # Dziś usłyszysz ... z Biblii,
   ("corpo_pl",6.27,9.55,17.80),   # która sprowadzi ... cudów.
   ("corpo_pl",9.55,11.80,22.80),  # Nie odrzucaj mnie... znowu.
   ("cta1_pl",0.0,3.34,25.60),     # Dotknij «Dowiedz się więcej» ... na żywo. (Dotknij sobre o fim da cena da cruz)
   ("cta2_pl",0.0,2.00,29.07)]     # Odbierz swój cud, zanim będzie za późno. (pausa ~0,45 s antes)
v=np.zeros((int(TOTAL*SR),2),np.float32); W=[]
fd=int(0.012*SR)
for n,a,b,t in P:
    x,pw=A[n]; s=x[int(a*SR):int(b*SR)].copy(); s[:fd]*=np.linspace(0,1,fd)[:,None]; s[-fd:]*=np.linspace(1,0,fd)[:,None]
    i=int(t*SR); v[i:i+len(s)]+=s[:len(v)-i]
    W+=[[w,round(ws-a+t,3),round(we-a+t,3)] for w,ws,we in pw if ws>=a-0.01 and we<=b+0.01]
sf.write("audio/voz_pl.wav",v,SR)
json.dump(W,open("palavras_pl.json","w",encoding="utf-8"),ensure_ascii=False)
for w in W: print(f"{w[1]:.2f}-{w[2]:.2f} {w[0]}")
for nm,a,b in [("hook",0.0,5.0667),("jb",5.0667,10.0),("cta",26.1,31.5)]:
    sf.write(f"heygen_in/{nm}_pl.wav",v[int(a*SR):int(b*SR)],SR)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"heygen_in/{nm}_pl.wav","-c:a","libmp3lame","-b:a","192k",f"heygen_in/{nm}_pl.mp3"])

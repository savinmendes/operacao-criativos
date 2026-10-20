# Voz EN na linha do tempo original (cortes de cena do ES mantidos). Gera audio/voz_en.wav, palavras_en.json e mp3 por trecho de lipsync
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; TOTAL=31.60
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
A={n:(load(f"audio/{n}.mp3"),palavras(f"audio/{n}.alinhamento.json")) for n in ["hook_en","b_en","corpo_en","cta_en"]}
# (arquivo, ini_no_arquivo, fim_no_arquivo, posição na linha do tempo)
P=[("hook_en",0.0,4.50,0.10),
   ("b_en",0.0,3.20,5.75),
   ("corpo_en",0.0,1.46,10.10),    # Jesus has chosen you.
   ("corpo_en",1.46,3.25,11.90),   # He has brought you a powerful gift.
   ("corpo_en",3.25,6.535,14.35),  # Today, you will hear an ancient, lost prayer from the Bible,
   ("corpo_en",6.535,10.0,17.95),  # that will unlock ... life.
   ("corpo_en",10.0,12.15,22.80),  # Do not reject me... again.
   ("cta_en",0.0,1.145,26.05),      # Tap Learn More below,
   ("cta_en",1.145,2.86,27.30),     # and join the live prayer right now.
   ("cta_en",2.86,4.85,29.15)]     # Receive your miracle, before it is too late.
v=np.zeros((int(TOTAL*SR),2),np.float32); W=[]
fd=int(0.012*SR)
for n,a,b,t in P:
    x,pw=A[n]; s=x[int(a*SR):int(b*SR)].copy(); s[:fd]*=np.linspace(0,1,fd)[:,None]; s[-fd:]*=np.linspace(1,0,fd)[:,None]
    i=int(t*SR); v[i:i+len(s)]+=s[:len(v)-i]
    W+=[[w,round(ws-a+t,3),round(we-a+t,3)] for w,ws,we in pw if ws>=a-0.01 and we<=b+0.01]
sf.write("audio/voz_en.wav",v,SR)
json.dump(W,open("palavras_en.json","w",encoding="utf-8"),ensure_ascii=False)
for w in W: print(f"{w[1]:.2f}-{w[2]:.2f} {w[0]}")
# trechos de lipsync: (nome, ini, fim) no tempo do original
for nm,a,b in [("hook",0.0,5.0667),("jb",5.0667,10.0),("cta",26.1,31.5)]:
    sf.write(f"heygen_in/{nm}_en.wav",v[int(a*SR):int(b*SR)],SR)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"heygen_in/{nm}_en.wav","-c:a","libmp3lame","-b:a","192k",f"heygen_in/{nm}_en.mp3"])

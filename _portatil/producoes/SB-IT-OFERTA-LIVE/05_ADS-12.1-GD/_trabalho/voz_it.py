# Voz IT na linha do tempo original (cortes de cena do ES mantidos). Gera audio/voz_it.wav, palavras_it.json e mp3 por trecho de lipsync
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; TOTAL=31.60
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
A={n:(load(f"audio/{n}.mp3"),palavras(f"audio/{n}.alinhamento.json")) for n in ["hook_it","b_it","corpo_it","cta_it"]}
P=[("hook_it",0.0,5.10,0.0),
   ("b_it",0.0,3.80,5.75),
   ("corpo_it",0.0,1.42,10.10),    # Gesù ti ha scelto.
   ("corpo_it",1.42,3.22,11.80),   # Ti ha portato un dono potente.
   ("corpo_it",3.22,6.03,14.35),   # Oggi ascolterai ... Bibbia,
   ("corpo_it",6.03,9.50,17.80),   # che sbloccherà ... vita.
   ("corpo_it",9.50,11.95,22.80),  # Non rifiutarmi... di nuovo.
   ("cta_it",0.0,2.94,25.75),      # Tocca «Scopri di più» ... in diretta. (Tocca sobre o fim da cena da cruz)
   ("cta_it",2.94,5.40,29.00)]     # Ricevi il tuo miracolo, prima che sia troppo tardi. (pausa ~0,45 s antes: boca fecha)
v=np.zeros((int(TOTAL*SR),2),np.float32); W=[]
fd=int(0.012*SR)
for n,a,b,t in P:
    x,pw=A[n]; s=x[int(a*SR):int(b*SR)].copy(); s[:fd]*=np.linspace(0,1,fd)[:,None]; s[-fd:]*=np.linspace(1,0,fd)[:,None]
    i=int(t*SR); v[i:i+len(s)]+=s[:len(v)-i]
    W+=[[w,round(ws-a+t,3),round(we-a+t,3)] for w,ws,we in pw if ws>=a-0.01 and we<=b+0.01]
sf.write("audio/voz_it.wav",v,SR)
json.dump(W,open("palavras_it.json","w",encoding="utf-8"),ensure_ascii=False)
for w in W: print(f"{w[1]:.2f}-{w[2]:.2f} {w[0]}")
for nm,a,b in [("hook",0.0,5.0667),("jb",5.0667,10.0),("cta",26.1,31.5)]:
    sf.write(f"heygen_in/{nm}_it.wav",v[int(a*SR):int(b*SR)],SR)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"heygen_in/{nm}_it.wav","-c:a","libmp3lame","-b:a","192k",f"heygen_in/{nm}_it.mp3"])

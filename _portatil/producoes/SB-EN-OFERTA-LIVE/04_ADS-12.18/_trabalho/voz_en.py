# Monta a voz EN na linha do tempo: gancho (corta em HK) + corpo com pausas dramáticas; gera alinhamento deslocado e cortes de cena
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; HK=3.20
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
h=load("audio/hook_en.mp3"); c=load("audio/corpo_en.mp3")
al=json.load(open("audio/corpo_en.alinhamento.json",encoding="utf-8"))
# pausas inseridas logo após o fim destas palavras (fim no alinhamento + 0.05)
P=[("way.",0.35),("you.",0.35),("you.",0.30),("miracles...",0.15),("again.",0.30),("now.",0.25)]
pw=palavras("audio/corpo_en.alinhamento.json")
ins=[]; j=0
for q,(w,s,e) in enumerate(pw):
    if j<len(P) and w==P[j][0]:
        nx=pw[q+1][1] if q+1<len(pw) else e+0.1
        ins.append(((e+nx)/2,P[j][1])); j+=1
assert j==len(P), ins
TAIL=1.0
out=[];prev=0
for t,d in ins:
    i=int(t*SR); out+=[c[prev:i],np.zeros((int(d*SR),2),np.float32)]; prev=i
fim=pw[-1][2]+0.15
out+=[c[prev:int(fim*SR)]]
corpo=np.concatenate(out)
sh=lambda x: x+sum(d for t,d in ins if x>=t)
al2={"characters":al["characters"],"character_start_times_seconds":[round(sh(x),3) for x in al["character_start_times_seconds"]],
     "character_end_times_seconds":[round(sh(x),3) for x in al["character_end_times_seconds"]]}
json.dump(al2,open("audio/corpo_en_p.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
TOTAL=round(HK+len(corpo)/SR+TAIL,2)
v=np.zeros((int(TOTAL*SR),2),np.float32); m=min(len(h),int(HK*SR)); v[:m]=h[:m]
fade=int(0.03*SR); v[m-fade:m]*=np.linspace(1,0,fade)[:,None]
v[int(HK*SR):int(HK*SR)+len(corpo)]=corpo
sf.write("audio/voz_en.wav",v,SR)
pw2=palavras("audio/corpo_en_p.alinhamento.json",HK)
inicio_frase=["Jesus","He","Today,","that","but","Tap","Receive"]
# cena 1 começa no HK; cada cena seguinte começa 0.10 s antes da primeira palavra
starts=[]; k=0
for w,s,e in pw2:
    if k<len(inicio_frase) and w==inicio_frase[k]: starts.append(round(s-0.10,2)); k+=1
C=[0,HK]+starts+[TOTAL]
json.dump(C,open("cortes_en.json","w")); print("cortes",C,"total",TOTAL)
for w,s,e in pw2: print(f"{s:.2f}-{e:.2f} {w}")

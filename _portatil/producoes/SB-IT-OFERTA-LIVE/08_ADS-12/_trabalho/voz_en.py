# Monta a voz EN na linha do tempo com pausas nas frases e calcula os cortes de cena (A..F) e a fonte de cada cena no ES
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
c=load("audio/voz_en_raw.mp3"); AL="audio/voz_en_raw.alinhamento.json"
al=json.load(open(AL,encoding="utf-8")); pw=palavras(AL)
# (palavra, ocorrencia, pausa extra) inserida no meio do vao depois dela
P=[("else.",0.30),("you.",0.40),("you.",0.12),("gift.",0.35),("life.",0.22),("again.",0.05),("below,",0.12)]
ins=[];j=0
for q,(w,s,e) in enumerate(pw):
    if j<len(P) and w==P[j][0]:
        nx=pw[q+1][1]; ins.append(((e+nx)/2,P[j][1])); j+=1
assert j==len(P),ins
INI=0.10; TAIL=0.75
out=[np.zeros((int(INI*SR),2),np.float32)];prev=0
for t,d in ins:
    i=int(t*SR); out+=[c[prev:i],np.zeros((int(d*SR),2),np.float32)]; prev=i
fim=pw[-1][2]+0.20; out+=[c[prev:int(fim*SR)]]
v=np.concatenate(out)
sh=lambda x: INI+x+sum(d for t,d in ins if x>=t)
al2={"characters":al["characters"],"character_start_times_seconds":[round(sh(x),3) for x in al["character_start_times_seconds"]],
     "character_end_times_seconds":[round(sh(x),3) for x in al["character_end_times_seconds"]]}
json.dump(al2,open("audio/voz_en_p.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
pw2=palavras("audio/voz_en_p.alinhamento.json")
def acha(w,k=1):
    n=0
    for x in pw2:
        if x[0]==w:
            n+=1
            if n==k: return x
    raise KeyError(w)
TOTAL=round(len(v)/SR+TAIL-0.20,2)
C=[0,round(acha("you.",1)[2]+0.30,2),round(acha("gift.")[2]+0.22,2),round(acha("that")[1]-0.10,2),
   round(acha("life.")[2]+0.10,2),round(acha("and",2)[1]-0.10,2),TOTAL]
tot=np.zeros((int(TOTAL*SR),2),np.float32); tot[:len(v)]=v[:len(tot)]
sf.write("audio/voz_en.wav",tot,SR)
ES=[0,10.0,14.6,18.67,22.97,26.1,31.5]
print("cortes",C,"total",TOTAL)
for k in range(6): print("cena",k,"dur",round(C[k+1]-C[k],2),"disp ES",round(ES[k+1]-ES[k],2))
json.dump({"C":C,"ES":ES},open("cortes_en.json","w"))
for w,s,e in pw2: print(f"{s:.2f}-{e:.2f} {w}")

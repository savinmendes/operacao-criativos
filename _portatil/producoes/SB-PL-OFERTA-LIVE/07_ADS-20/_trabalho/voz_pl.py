# Linha do tempo da voz PL: gancho Jesus (2 frases nos tempos do ES) + corpo (Brian) a partir de 4.38 com pausas de paragrafo
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; HK=4.267; C0=4.38; PAUSA=0.20; TAIL=0.7
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
h1=load("audio/hook1_pl.mp3"); h2=load("audio/hook2_pl.mp3"); c=load("audio/corpo_pl.mp3")
al=json.load(open("audio/corpo_pl.alinhamento.json",encoding="utf-8"))
ch=al["characters"]; cs=al["character_start_times_seconds"]; ce=al["character_end_times_seconds"]
# pontos de pausa: entre o fim do paragrafo e a 1a letra do seguinte
pw=palavras("audio/corpo_pl.alinhamento.json")
fins=[l.strip().split()[-1] for l in open("audio/corpo_pl.txt",encoding="utf-8") if l.strip()][:-1]
cont=[len([1 for l in open("audio/corpo_pl.txt",encoding="utf-8") if l.strip()])]
# indice global da ultima palavra de cada paragrafo
idx=[];n=0
for l in open("audio/corpo_pl.txt",encoding="utf-8"):
    if l.strip(): n+=len(l.split()); idx.append(n-1)
ins=[]
for q in idx[:-1]:
    assert pw[q][0]==fins[len(ins)], (pw[q],fins[len(ins)])
    ins.append(((pw[q][2]+pw[q+1][1])/2,PAUSA))
pw=palavras("audio/corpo_pl.alinhamento.json")
out=[];prev=0
for t,d in ins:
    k=int(t*SR); out+=[c[prev:k],np.zeros((int(d*SR),2),np.float32)]; prev=k
fim=pw[-1][2]+0.2; out+=[c[prev:int(fim*SR)]]
corpo=np.concatenate(out)
sh=lambda x: x+sum(d for t,d in ins if x>=t)
al2={"characters":ch,"character_start_times_seconds":[round(sh(x),3) for x in cs],"character_end_times_seconds":[round(sh(x),3) for x in ce]}
json.dump(al2,open("audio/corpo_pl_p.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
TOTAL=round(C0+len(corpo)/SR+TAIL,2)
v=np.zeros((int(TOTAL*SR)+10,2),np.float32)
def put(x,t): i=int(t*SR); v[i:i+len(x)]+=x
put(h1,0.08); put(h2,2.55); put(corpo,C0)
sf.write("audio/voz_pl.wav",v,SR)
# trilha do gancho p/ HeyGen (so o trecho do gancho)
sf.write("audio/hook_pl_heygen.wav",v[:int(HK*SR)],SR)
json.dump({"TOTAL":TOTAL,"HK":HK,"C0":C0,"pausas":ins},open("tempos.json","w"),indent=0)
print("TOTAL",TOTAL,"pausas",len(ins),"h1",len(h1)/SR,"h2 fim",2.55+len(h2)/SR)

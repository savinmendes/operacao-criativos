# Voz PL (eleven_multilingual_v2 + language_code pl, Jesus The Chosen): encurta pausas, atempo, calcula cortes de cena A..F
import soundfile as sf, numpy as np, subprocess, json, sys
from palavras import palavras
SR=48000; TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.04
RAW="audio/voz_pl_raw.mp3"; AL="audio/voz_pl_raw.alinhamento.json"
def load(p,af=None):
    cmd=["ffmpeg","-v","error","-i",p]+(["-af",af] if af else [])+["-ac","2","-ar",str(SR),"-f","f32le","-"]
    raw=subprocess.run(cmd,capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
pw=palavras(AL)
G=0.20; ESP={"potrzebujesz.":0.15,"przygotowałem.":0.32,"wybrał.":0.28,"dar.":0.32,"Biblii,":0.12,"cudów.":0.30,"znowu.":0.18,'więcej"':0.14,"poniżej":0.12,"żywo.":0.22}
# novo tempo de cada palavra (no raw): remove silencio no meio de cada vao
rem=[]  # (inicio_raw, fim_raw) a remover
for q in range(len(pw)-1):
    w,s,e=pw[q]; nx=pw[q+1][1]; gap=nx-e; want=ESP.get(w,G)
    if gap>want+0.01:
        mid=(e+nx)/2; d=gap-want; rem.append((mid-d/2,mid+d/2))
c=load(RAW)
keep=[];prev=0
for a,b in rem: keep.append(c[int(prev*SR):int(a*SR)]); prev=b
fim=pw[-1][2]+0.15; keep.append(c[int(prev*SR):int(fim*SR)])
v=np.concatenate(keep); sf.write("audio/_tmp_c.wav",v,SR)
v=load("audio/_tmp_c.wav",f"atempo={TEMPO}")
INI=0.06
def sh(x):
    r=x-sum(min(b,max(a,x))-a for a,b in rem)
    return INI+r/TEMPO
al=json.load(open(AL,encoding="utf-8"))
al2={"characters":al["characters"],"character_start_times_seconds":[round(sh(x),3) for x in al["character_start_times_seconds"]],
     "character_end_times_seconds":[round(sh(x),3) for x in al["character_end_times_seconds"]]}
json.dump(al2,open("audio/voz_pl_p.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
pw2=palavras("audio/voz_pl_p.alinhamento.json")
def acha(w,k=1):
    n=0
    for x in pw2:
        if x[0]==w:
            n+=1
            if n==k: return x
    raise KeyError(w)
TOTAL=round(acha("późno.")[2]+0.45,2)
C=[0,round(acha("przygotowałem.")[2]+0.12,2),round(acha("dar.")[2]+0.22,2),round(acha("która")[1]-0.08,2),
   round(acha("cudów.")[2]+0.12,2),round(acha("poniżej")[1]-0.07,2),TOTAL]
tot=np.zeros((int(TOTAL*SR),2),np.float32); vv=np.concatenate([np.zeros((int(INI*SR),2),np.float32),v]); tot[:min(len(vv),len(tot))]=vv[:len(tot)]
sf.write("audio/voz_pl.wav",tot,SR)
ES=[0,10.0,14.6,18.67,22.97,26.1,31.5]
print("cortes",C,"total",TOTAL)
for k in range(6): print("cena",k,"dur",round(C[k+1]-C[k],2),"disp ES",round(ES[k+1]-ES[k],2),"vel",round(min(1,(ES[k+1]-ES[k])/(C[k+1]-C[k])),2))
json.dump({"C":C,"ES":ES},open("cortes_pl.json","w"))

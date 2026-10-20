"""Emendas sem custo: corta trecho do áudio (remove) ou junta prefixo regenerado. Atualiza alinhamento por caractere."""
import json, subprocess, sys
import numpy as np
from pathlib import Path
SR = 44100
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",str(p),"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
def save(x,p):
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-","-c:a","libmp3lame","-b:a","192k",str(p)],input=x.astype(np.float32).tobytes(),check=True)
def al(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def fade_join(a,b,xf=0.012):
    n=int(xf*SR); a=a.copy(); b=b.copy()
    a[-n:]*=np.linspace(1,0,n); b[:n]*=np.linspace(0,1,n); return np.concatenate([a,b])
def corta(src, a, b, dst):
    x=load(src+".mp3"); d=al(src+".alinhamento.json")
    y=fade_join(x[:int(a*SR)], x[int(b*SR):]); save(y,dst+".mp3")
    dd=b-a; K=("character_start_times_seconds","character_end_times_seconds")
    for k in K: d[k]=[t if t<=a else (a if t<b else t-dd) for t in d[k]]
    Path(dst+".alinhamento.json").write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
def prefixo(pre, pre_fim, src, src_ini, dst, gap=0.03):
    p=load(pre+".mp3")[:int(pre_fim*SR)]; x=load(src+".mp3")[int(src_ini*SR):]
    y=fade_join(np.concatenate([p,np.zeros(int(gap*SR),np.float32)]), x); save(y,dst+".mp3")
    dp=al(pre+".alinhamento.json"); ds=al(src+".alinhamento.json"); off=pre_fim+gap-src_ini
    i=next(k for k,t in enumerate(ds["character_start_times_seconds"]) if t>=src_ini-0.02)
    out={"characters":dp["characters"]+[" "]+ds["characters"][i:],
         "character_start_times_seconds":[min(t,pre_fim) for t in dp["character_start_times_seconds"]]+[pre_fim]+[t+off for t in ds["character_start_times_seconds"][i:]],
         "character_end_times_seconds":[min(t,pre_fim) for t in dp["character_end_times_seconds"]]+[pre_fim]+[t+off for t in ds["character_end_times_seconds"][i:]]}
    Path(dst+".alinhamento.json").write_text(json.dumps(out,ensure_ascii=False),encoding="utf-8")
if __name__=="__main__":
    c=sys.argv[1]
    if c=="corta": corta(sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),sys.argv[5])
    else: prefixo(sys.argv[2],float(sys.argv[3]),sys.argv[4],float(sys.argv[5]),sys.argv[6])

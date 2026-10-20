# Troca os paragrafos 10 e 13 do corpo v1 pelas regravacoes (p10/p13), cortando no meio das pausas entre paragrafos
import json, subprocess, numpy as np, soundfile as sf
SR=44100
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
old=load("v1/corpo_it.mp3"); A=json.load(open("v1/corpo_it.alinhamento.json",encoding="utf-8"))
Lold=[l.strip() for l in open("v1/corpo_it.txt",encoding="utf-8") if l.strip()]
Lnew=[l.strip() for l in open("audio/corpo_it.txt",encoding="utf-8") if l.strip()]
ch=A["characters"]; cs=A["character_start_times_seconds"]; ce=A["character_end_times_seconds"]
assert "".join(ch)==" ".join(Lold), "alinhamento != texto"
# faixa de chars de cada paragrafo
rng=[];p=0
for l in Lold: rng.append((p,p+len(l))); p+=len(l)+1
def seg_old(i):  # (start,end) de fala do paragrafo i
    a,b=rng[i]; return cs[a],ce[b-1]
pieces=[]  # (audio, chars, starts, ends)
t_cursor=0.0; out_audio=[]; oc=[];os_=[];oe=[]
REP={10:"audio/p10",13:"audio/p13"}
# cortes: meio da pausa entre paragrafo i-1 e i
cut=[0.0]+[(seg_old(i-1)[1]+seg_old(i)[0])/2 for i in range(1,len(Lold))]+[len(old)/SR]
for i,l in enumerate(Lold):
    a,b=rng[i]
    if i not in REP:
        t0,t1=cut[i],cut[i+1]; x=old[int(t0*SR):int(t1*SR)]
        C=ch[a:b]; S=[s-t0 for s in cs[a:b]]; E=[e-t0 for e in ce[a:b]]
    else:
        n=load(REP[i]+".mp3"); B=json.load(open(REP[i]+".alinhamento.json",encoding="utf-8"))
        assert "".join(B["characters"]).strip()==Lnew[i]
        s0,e0=seg_old(i); pre=s0-cut[i]; post=cut[i+1]-e0
        bc=B["characters"]; k0=next(k for k,c in enumerate(bc) if not c.isspace()); k1=max(k for k,c in enumerate(bc) if not c.isspace())
        ns,ne=B["character_start_times_seconds"][k0],B["character_end_times_seconds"][k1]
        seg=n[max(0,int((ns-0.03)*SR)):int((ne+0.06)*SR)]
        fade=int(0.02*SR); seg=seg.copy(); seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
        x=np.concatenate([np.zeros(int((pre-0.03)*SR),np.float32),seg,np.zeros(int((post-0.06)*SR),np.float32)])
        off=pre-ns
        C=bc[k0:k1+1]; S=[s+off for s in B["character_start_times_seconds"][k0:k1+1]]; E=[e+off for e in B["character_end_times_seconds"][k0:k1+1]]
    if i>0: oc.append(" "); os_.append(t_cursor); oe.append(t_cursor)
    oc+=C; os_+=[s+t_cursor for s in S]; oe+=[e+t_cursor for e in E]
    out_audio.append(x); t_cursor+=len(x)/SR
assert "".join(oc)==" ".join(Lnew)
y=np.concatenate(out_audio)
sf.write("audio/corpo_it_splice.wav",y,SR)
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/corpo_it_splice.wav","-c:a","libmp3lame","-b:a","192k","audio/corpo_it.mp3"],check=True)
json.dump({"characters":oc,"character_start_times_seconds":[round(v,3) for v in os_],"character_end_times_seconds":[round(v,3) for v in oe]},open("audio/corpo_it.alinhamento.json","w",encoding="utf-8"),ensure_ascii=False)
print("v1",round(len(old)/SR,2),"novo",round(len(y)/SR,2))

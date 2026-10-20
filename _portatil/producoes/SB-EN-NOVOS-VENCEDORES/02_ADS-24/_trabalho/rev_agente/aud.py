import json, numpy as np, soundfile as sf
x,sr=sf.read("rev_agente/a48.wav"); 
m,sr2=sf.read("audio/mix_en.wav"); m=m.mean(1) if m.ndim>1 else m
print("dur final",len(x)/sr,"mix",len(m)/sr2)
# offset via xcorr on envelope windows
def env(a,sr,hop=480): n=len(a)//hop; return np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))
ef=env(x,sr); em=env(m,sr2)
for t0 in [2,30,52,80,110]:
    i=int(t0*100); seg=ef[i:i+300]
    best=max(range(-50,51),key=lambda k: np.corrcoef(seg,em[i+k:i+k+300])[0,1] if i+k>=0 else -1)
    print("t",t0,"lag(10ms)",best, round(np.corrcoef(seg,em[i+best:i+best+300])[0,1],3))
db=lambda a: 20*np.log10(np.sqrt((a**2).mean())+1e-9)
w=json.load(open("rev_agente/words_medium.json"))
def speechdb(t0,t1):
    segs=[x[int(a*sr):int(b*sr)] for a,b,_,_ in w if a>=t0 and b<=t1]
    return db(np.concatenate(segs))
print("velho voz dB",round(speechdb(0,4.7),1),"anjo 5.7-30",round(speechdb(5.7,30),1),"anjo 30-60",round(speechdb(30,60),1),"anjo 60-122",round(speechdb(60,122.1),1))
# gaps
print("gaps >0.25s: level dB")
for (a0,b0,t0_,_),(a1,b1,t1_,_) in zip(w,w[1:]):
    if a1-b0>0.25:
        g=x[int((b0+0.06)*sr):int((a1-0.04)*sr)]
        if len(g)>sr*0.1: print(f"  {b0:.2f}-{a1:.2f} {db(g):.1f} dB  peak {20*np.log10(np.abs(g).max()+1e-9):.1f}")
print("fim: ultimos 0.5s dB",round(db(x[-sr//2:]),1),"ultimos 0.1s",round(db(x[-sr//10:]),1))
print("ultimo word end",w[-1])

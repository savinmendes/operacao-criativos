# piso de ruído 7-14 kHz (dBFS RMS) nas pausas da fala. uso: piso.py arquivo [palavras.json] [desloc_cortes]
import sys,json,subprocess,numpy as np
from scipy.signal import butter,sosfiltfilt
def load(p,sr=48000):
    r=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(r,np.float32).copy(),sr
def pausas(W,total,cut=False):
    ev=sorted((s,e) for w,s,e,p in W)
    if cut:  # mapeia para a linha do tempo pós jump-cut (quadros 386-401 e 465-478 removidos)
        def m(t):
            if t>=479/30: return t-30/30
            if t>=402/30: return t-16/30
            return t
        ev=[(m(s),m(e)) for s,e in ev]
    P=[];prev=0.0
    for s,e in ev:
        if s-prev>0.30: P.append((prev+0.08,s-0.08))
        prev=max(prev,e)
    return P
def piso(x,sr,P):
    sos=butter(8,[7000,14000],btype="band",fs=sr,output="sos"); y=sosfiltfilt(sos,x)
    v=[np.mean(y[int(a*sr):int(b*sr)]**2) for a,b in P if b-a>0.1 and int(b*sr)<=len(y)]
    return 10*np.log10(np.median(v)+1e-20), 10*np.log10(np.mean(v)+1e-20), len(v)
if __name__=="__main__":
    x,sr=load(sys.argv[1]); W=json.load(open(sys.argv[2] if len(sys.argv)>2 else "../palavras_fr.json",encoding="utf-8"))
    P=pausas(W,len(x)/sr,cut=len(sys.argv)>3 and sys.argv[3]=="cut")
    med,mean,n=piso(x,sr,P); print(f"{sys.argv[1]}: piso 7-14k pausas mediana {med:.1f} dBFS, media {mean:.1f} ({n} pausas)")

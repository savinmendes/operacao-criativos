"""Monta o leito musical de duracao exata: pula intro fraca (inicio em batida) e, antes do outro natural
da trilha, emenda um trecho anterior alinhado em batida (crossfade 60 ms). Uso: python leito.py A 48.07"""
import sys,numpy as np,librosa,soundfile as sf
n=sys.argv[1]; dur=float(sys.argv[2])
INI={"A":4.8,"B":1.9,"C":0.0}; CORTE_MAX={"A":44.0,"B":44.5,"C":44.0}
y,sr=librosa.load(f"trilha_{n}.mp3",sr=48000,mono=False)
mono=librosa.to_mono(y)
_,b=librosa.beat.beat_track(y=librosa.resample(mono,orig_sr=48000,target_sr=22050),sr=22050,units="time")
snap=lambda t:b[np.argmin(abs(b-t))]
s0=snap(INI[n]) if INI[n]>0 else 0.0
# ponto de corte na fonte: a ultima batida <= CORTE_MAX
ib=np.where(b<=CORTE_MAX[n])[0][-1]; tc=b[ib]; ts=b[ib-32]
seg1=y[:,int(s0*sr):int(tc*sr)]
falta=dur-seg1.shape[1]/sr+0.2
seg2=y[:,int(ts*sr):int((ts+falta)*sr)]
xf=int(0.06*sr); w=np.linspace(0,1,xf)
out=np.concatenate([seg1[:,:-xf], seg1[:,-xf:]*np.cos(w*np.pi/2)+seg2[:,:xf]*np.sin(w*np.pi/2), seg2[:,xf:]],axis=1)[:,:int(dur*sr)]
sf.write(f"_leito_{n}.wav",out.T,sr)
print(n,f"inicio {s0:.2f}s, emenda em {seg1.shape[1]/sr:.2f}s do leito (fonte {tc:.2f}->{ts:.2f}), dur {out.shape[1]/sr:.2f}")

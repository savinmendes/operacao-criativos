import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
from scipy.signal import stft
for p in sys.argv[1:]:
    x=load(p,ch=1); f,t,Z=stft(x,SR,nperseg=1024,noverlap=768); P=np.abs(Z)**2
    tot=10*np.log10(P.sum(0)+1e-20); act=tot>tot.max()-70
    lo=10*np.log10(P[(f>150)&(f<4000)].mean(0)+1e-20); hi=10*np.log10(P[(f>7000)&(f<14000)].mean(0)+1e-20)
    print(p[-30:], "frames ativos",act.sum(),"/",len(act))
    for q in (5,10,20,50,90): print("  q",q,"hi",round(np.percentile(hi[act],q),1),"lo",round(np.percentile(lo[act],q),1))
    # perfil por banda (percentil 10 dos ativos)
    N=np.percentile(P[:,act],10,axis=1); M=np.percentile(P[:,act],50,axis=1)
    for a,b in [(100,500),(500,2000),(2000,4000),(4000,7000),(7000,10000),(10000,14000),(14000,16000)]:
        k=(f>=a)&(f<b); print(f"  {a}-{b}: p10 {10*np.log10(N[k].mean()):.1f}  p50 {10*np.log10(M[k].mean()):.1f}")

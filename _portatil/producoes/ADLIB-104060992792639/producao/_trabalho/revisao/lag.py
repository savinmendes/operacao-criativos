import sys, csv, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
AD=sys.argv[1]; T=Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho")/AD
rows=list(csv.DictReader(open(f"boca_{AD}.csv"))); N=len(rows)
col=lambda k: np.array([float(r[k]) if r[k]!="" else np.nan for r in rows])
abf,abo=col("ab_f"),col("ab_o")
env=lambda p: cl.envelope(cl.ler_audio(p),16000,30.0,N)
es=env(T/"narracao_es.wav"); pt=env(T/"_audio/demucs/htdemucs/orig/vocals.wav")
def hp(x,k=31):
    m=np.isfinite(x); xi=np.interp(np.arange(len(x)),np.where(m)[0],x[m])
    xi=np.convolve(xi,np.ones(3)/3,"same")
    return xi-np.convolve(xi,np.ones(k)/k,"same")
for nome,a,s in (("final x ES",abf,es),("final x PT",abf,pt),("orig x PT",abo,pt),("orig x ES",abo,es)):
    A=hp(a); S=hp(s)
    res=[]
    for lag in range(-30,31,2):
        if lag>=0: x,y=A[:N-lag],S[lag:]
        else: x,y=A[-lag:],S[:N+lag]
        res.append((lag,np.corrcoef(x,y)[0,1]))
    best=max(res,key=lambda r:r[1]); z=[c for l,c in res if l==0][0]
    print(f"{nome}: corr lag0 {z:.3f} | melhor {best[1]:.3f} em {best[0]*33:+d} ms | "+" ".join(f"{c:.2f}" for l,c in res[::3]))

import sys, json, numpy as np
sys.path.insert(0, r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
d=json.load(open(sys.argv[1])); fps=d['fps']
ab=np.array([np.nan if a is None else a for a in d['ab']]); env=np.array(d['env'])
fala=cl.mascara_fala(env); pausa=cl.mascara_pausas(fala)
tot=[]
for r in sys.argv[2:]:
    a,b=[int(round(float(x)*fps)) for x in r.split('-')]
    seg=ab[a:b]; ok=np.isfinite(seg); mp_=pausa[a:b]&ok; mf=fala[a:b]&ok
    tot.append((seg[mp_].sum(),mp_.sum(),seg[mf].sum(),mf.sum()))
    idx = seg[mp_].mean()/seg[mf].mean() if mp_.sum()>=4 and mf.sum()>=10 else None
    pt=[round(i/fps+a/fps,2) for i in np.nonzero(mp_)[0]]
    print(f'{r:12s} rosto {ok.mean():.0%} fala {mf.sum():3d}q ab {np.nanmean(seg[mf]) if mf.sum() else 0:.3f} | pausa {mp_.sum():3d}q ab {np.nanmean(seg[mp_]) if mp_.sum() else float("nan"):.3f} | indice {None if idx is None else round(float(idx),2)}  pausas {pt[:1]}..{pt[-1:]}')
t=np.array(tot).sum(0); print('CONJUNTO indice', round(float((t[0]/t[1])/(t[2]/t[3])),2), 'pausa q', int(t[1]))

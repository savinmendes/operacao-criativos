import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
from pathlib import Path
video, voc, out = sys.argv[1], sys.argv[2], sys.argv[3]
fps, ab, _, _, _ = cl.series_video(Path(video), None)
x, sr = sf.read(voc); x = x.mean(1)
env = cl.envelope(x, sr, fps, len(ab))
json.dump({'fps':fps,'ab':[None if not np.isfinite(a) else round(float(a),4) for a in ab],'env':env.round(2).tolist()}, open(out,'w'))
ok = np.isfinite(ab)
runs=[];s=None
for i,v in enumerate(list(ok)+[False]):
    if v and s is None: s=i
    if not v and s is not None:
        if i-s>=15: runs.append((s,i))
        s=None
print('face runs', [(round(a/fps,2), round(b/fps,2)) for a,b in runs])
fala_all = cl.mascara_fala(env)
for a,b in runs:
    s = cl.somas_pausa(ab[a:b], env[a:b])
    # use global speech threshold instead of per-segment
    fala = fala_all[a:b]; pausa = cl.mascara_pausas(fala); okk = np.isfinite(ab[a:b])
    mp_, mf = pausa&okk, fala&okk
    idx = (ab[a:b][mp_].mean()/ab[a:b][mf].mean()) if mp_.sum()>=4 and mf.sum()>=10 else None
    print(f'  {a/fps:6.2f}-{b/fps:6.2f}  ab_fala {np.nanmean(ab[a:b][mf]) if mf.sum() else float("nan"):.3f}  ab_pausa {np.nanmean(ab[a:b][mp_]) if mp_.sum() else float("nan"):.3f}  n_pausa {int(mp_.sum())}  indice {None if idx is None else round(float(idx),2)}')

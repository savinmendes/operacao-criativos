import sys, numpy as np
import medir as Me
from pathlib import Path
AD = Path(__file__).resolve().parent.parent
clip, q0 = sys.argv[1], int(sys.argv[2])
ab = Me.aberturas(clip)
es = Me.env("es", AD / "narracao_es.wav"); pt = Me.env("pt", AD / "_audio/demucs/htdemucs/orig/vocals.wav")
m = np.isfinite(ab); x = np.interp(np.arange(len(ab)), np.where(m)[0], ab[m]); x = np.convolve(x, np.ones(3)/3, "same")
for nm, e in (("ES", es), ("PT", pt)):
    best = []
    for lag in range(-45, 46, 3):
        a0 = q0 + lag; y = e[a0:a0+len(x)]
        if a0 < 0 or len(y) < len(x): continue
        best.append((np.corrcoef(x, y)[0, 1], lag))
    best.sort(reverse=True)
    print(nm, "lag0=%.2f" % dict((l, c) for c, l in best).get(0, np.nan), "melhores:", [(round(c, 2), round(l / 30, 2)) for c, l in best[:4]])

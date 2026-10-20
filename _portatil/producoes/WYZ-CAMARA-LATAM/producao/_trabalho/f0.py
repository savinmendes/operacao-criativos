import sys, librosa, numpy as np
y, sr = librosa.load(sys.argv[1], sr=16000, mono=True)
f0, v, p = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
f = f0[v & ~np.isnan(f0)]
print(sys.argv[1], 'mediana F0 = %.0f Hz' % np.median(f), 'n=', len(f))

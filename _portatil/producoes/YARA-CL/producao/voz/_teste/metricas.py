import numpy as np, librosa, glob, sys
def met(p):
    y, sr = librosa.load(p, sr=22050)
    yt, _ = librosa.effects.trim(y, top_db=35)
    f0, v, _ = librosa.pyin(yt, fmin=100, fmax=500, sr=sr, frame_length=2048, hop_length=256)
    f = f0[v]
    cen = librosa.feature.spectral_centroid(y=yt, sr=sr).mean()
    return len(y)/sr, np.nanmedian(f), np.nanstd(f), cen
arqs = ["gancho.wav"] + sys.argv[1:]
for a in arqs:
    d, f, s, c = met(a)
    print(f"{a:28s} dur={d:5.2f}s  f0_med={f:5.0f}Hz  f0_sd={s:4.0f}  centroide={c:5.0f}")

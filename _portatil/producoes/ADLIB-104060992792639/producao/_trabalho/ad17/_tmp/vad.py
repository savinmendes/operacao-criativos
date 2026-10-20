import sys, numpy as np, librosa
p = sys.argv[1]; y, sr = librosa.load(p, sr=16000, mono=True)
hop = 160; e = librosa.feature.rms(y=y, frame_length=640, hop_length=hop)[0]
db = 20 * np.log10(e + 1e-9); thr = np.percentile(db, 95) - 30
on = db > thr; segs = []; i = 0; n = len(on)
while i < n:
    if on[i]:
        j = i
        while j < n and on[j]: j += 1
        segs.append([i * hop / sr, j * hop / sr]); i = j
    else: i += 1
m = []
for s in segs:
    if m and s[0] - m[-1][1] < float(sys.argv[2] if len(sys.argv) > 2 else 0.25): m[-1][1] = s[1]
    else: m.append(s)
m = [s for s in m if s[1] - s[0] > 0.12]
for s in m: print(f"{s[0]:.2f}-{s[1]:.2f}")

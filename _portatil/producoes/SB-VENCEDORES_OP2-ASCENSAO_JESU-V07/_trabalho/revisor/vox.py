import sys, numpy as np, soundfile as sf
for v in sys.argv[1:]:
    x, sr = sf.read(f'demucs/htdemucs/{v}/vocals.wav'); x = x.mean(1)
    m, _ = sf.read(f'demucs/htdemucs/{v}/no_vocals.wav'); m = m.mean(1)
    hop = sr//100
    def env(a): return 20*np.log10(np.sqrt(np.convolve(a**2, np.ones(hop*3)/(hop*3), 'same')[::hop])+1e-9)
    e = env(x); em = env(m)
    pk = np.percentile(e, 99)
    on = e > pk-30
    # merge gaps < 0.12s, drop blips <0.06s
    segs=[]; i=0; n=len(on)
    while i<n:
        if on[i]:
            j=i
            while j<n and on[j]: j+=1
            segs.append([i,j]); i=j
        else: i+=1
    mg=[]
    for s in segs:
        if mg and s[0]-mg[-1][1] < 12: mg[-1][1]=s[1]
        else: mg.append(s)
    mg=[s for s in mg if s[1]-s[0]>=6]
    print('==',v,'peak env',round(pk,1))
    print(' '.join(f'[{a/100:.2f}-{b/100:.2f}]' for a,b in mg))
    sp = on
    print('voice rms (speech frames) dB', round(np.mean(e[sp]),1), ' music rms during speech dB', round(np.mean(em[sp]),1), ' music during pauses dB', round(np.mean(em[~sp]),1))
    print('last voice end', mg[-1][1]/100, 'duration', len(x)/sr)

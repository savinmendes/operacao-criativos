import numpy as np, subprocess, sys
def env(p, hop=0.01, sr=16000):
    x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(sr),"-f","s16le","-"],capture_output=True).stdout, np.int16).astype(np.float32)/32768
    h=int(hop*sr); n=len(x)//h
    r = np.sqrt((x[:n*h].reshape(n,h)**2).mean(1)+1e-12)
    return 20*np.log10(r)
def regioes(p, thr_rel=-35, min_sil=0.08):
    e=env(p); mx=np.percentile(e,99); on = e>mx+thr_rel
    reg=[]; i=0
    while i<len(on):
        if on[i]:
            j=i
            while j<len(on) and on[j]: j+=1
            reg.append([i/100,j/100]); i=j
        else: i+=1
    m=[]
    for a,b in reg:
        if m and a-m[-1][1]<min_sil: m[-1][1]=b
        else: m.append([a,b])
    return [r for r in m if r[1]-r[0]>=0.04]
if __name__=="__main__":
    for p in sys.argv[1:]:
        print(p, " ".join(f"{a:.2f}-{b:.2f}" for a,b in regioes(p)))

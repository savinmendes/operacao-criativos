import subprocess, numpy as np, sys, json
def frames(p, w=180, h=320):
    cmd=['ffmpeg','-v','error','-i',p,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-']
    raw=subprocess.run(cmd,capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(np.float32)
for name,p in [('v3',sys.argv[1]),('v1',sys.argv[2])]:
    f=frames(p)
    d=np.abs(np.diff(f,axis=0)).mean(axis=(1,2))
    np.save(name+'_diff.npy',d); np.save(name+'_luma.npy',f.mean(axis=(1,2)))
    print(name,len(f))
    cuts=[i+1 for i in range(len(d)) if d[i]>12 and d[i]>3*np.median(d[max(0,i-5):i+6])]
    print('cuts',[(c,round(c/30,3),round(float(d[c-1]),1)) for c in cuts])
    gaps=np.diff([0]+cuts+[len(f)])
    print('short scenes',[(cuts[i-1] if i>0 else 0,int(g)) for i,g in enumerate(gaps) if g<=3])
    z=[i+1 for i in range(len(d)) if d[i]<0.05]
    print('frozen-ish count',len(z))

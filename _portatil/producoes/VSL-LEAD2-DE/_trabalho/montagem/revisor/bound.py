import subprocess,numpy as np
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
W,H=180,240
def frames(a,d):
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-vf",f"scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    return np.frombuffer(r,np.uint8).reshape(-1,H,W).astype(np.float32)
def audio(a,d):
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(r,np.float32)
for B in range(300,2300,300):
    f=frames(B-1.5,3); d=np.abs(np.diff(f,axis=0)).mean(axis=(1,2))
    t=[round(B-1.5+(i+1)/30,3) for i in range(len(d))]
    dups=[t[i] for i in range(len(d)) if d[i]<0.05]
    big=[(t[i],round(float(d[i]),1)) for i in range(len(d)) if d[i]>8]
    a=audio(B-1,2); x=a; dd=np.abs(np.diff(x)); 
    w=int(0.05*48000); c=48000
    loc=dd[c-w:c+w]; base=np.median(dd)+1e-9
    rms=[float(np.sqrt(np.mean(x[i:i+480]**2))) for i in range(c-4800,c+4800,480)]
    print(f"B={B}s ({B//60}:{B%60:02d}) nframes={len(f)} diff_med={np.median(d):.2f} dups={dups[:10]}{'...' if len(dups)>10 else ''} bigjumps={big} | audio maxdiff@±50ms={loc.max():.4f} vs median={base:.5f} p99.9={np.percentile(dd,99.9):.4f} rms10ms(-100..+100ms)={[round(r,3) for r in rms]}")

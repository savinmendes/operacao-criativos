import subprocess,numpy as np,cv2
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
def frames(a,d):
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    return np.frombuffer(r,np.uint8).reshape(-1,960,720)
def audio(a,d):
    r=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(d),"-i",V,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(r,np.float32)
segs=[(121,8,(280,380,270,340)),(251,8,(290,410,675,750)),(287,8,(320,420,320,385)),(546,8,(280,380,230,295)),(1111,8,(260,360,240,305)),(1641,8,(275,365,212,272)),(2011,8,(310,430,235,310)),(2271,8,(300,420,265,340))]
for a,d,R in segs:
    f=frames(a,d)
    mx0,mx1,my0,my1=R; x=y=w=h=0
    roi=f[:,my0:my1,mx0:mx1].astype(np.float32)
    # openness proxy: fraction of dark pixels (mouth cavity) relative to roi median
    open_=np.array([(r<np.percentile(r,50)*0.6).mean() for r in roi])
    motion=np.r_[0,np.abs(np.diff(roi,axis=0)).mean(axis=(1,2))]
    au=audio(a,d); n=len(f)
    env=np.array([np.sqrt(np.mean(au[int(i*1600):int((i+1)*1600)]**2)) if int((i+1)*1600)<=len(au) else 0 for i in range(n)])
    def z(v): v=v-v.mean(); return v/(v.std()+1e-9)
    res=[]
    for sig,name in [(open_,'open'),(motion,'motion')]:
        best=[]
        for lag in range(-12,13):
            # positive lag: video lags audio by lag frames
            if lag>=0: c=np.corrcoef(z(sig)[lag:],z(env)[:n-lag])[0,1]
            else: c=np.corrcoef(z(sig)[:n+lag],z(env)[-lag:])[0,1]
            best.append((c,lag))
        best.sort(reverse=True); c0=[c for c,l in best if l==0][0]
        res.append(f"{name}: best lag={best[0][1]:+d}f ({best[0][1]*33:+d}ms) r={best[0][0]:.2f}, r@0={c0:.2f}")
    print(f"{a//60:02d}:{a%60:02d}-{(a+d)//60:02d}:{(a+d)%60:02d} face={x,y,w,h} | "+" | ".join(res),flush=True)

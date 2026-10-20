import subprocess, numpy as np, sys
V=r"C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\02_ADS-7\SB-IT-ADS-7.mp4"
W,H=270,480
def frames(t0,n):
    p=subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-i",V,"-frames:v",str(n),"-vf",f"scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    return np.frombuffer(p,np.uint8).reshape(-1,H,W,3).astype(float)
for c in [4.80,13.75]:
    f=frames(c-0.3,18)
    d=[np.abs(f[i+1]-f[i]).mean() for i in range(len(f)-1)]
    face=[np.abs(f[i+1][165:320,120:250]-f[i][165:320,120:250]).mean() for i in range(len(f)-1)]
    lum=[f[i].mean() for i in range(len(f))]
    print(c,"diff",[round(x,1) for x in d]);print(" face",[round(x,1) for x in face]);print(" lum",[round(x,1) for x in lum])

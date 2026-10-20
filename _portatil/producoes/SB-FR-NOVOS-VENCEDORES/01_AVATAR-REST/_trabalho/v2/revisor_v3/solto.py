import subprocess,numpy as np,sys
def frames(p,w=135,h=240):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(np.float32)
f=frames(sys.argv[1])
# blocks 15x15 px tiles
H,W=240,135
for i in range(1,len(f)-1):
    a=np.abs(f[i]-f[i-1]); b=np.abs(f[i+1]-f[i]); c=np.abs(f[i+1]-f[i-1])
    # tile max
    def tm(x): return x[:225,:135].reshape(15,15,9,15).mean(axis=(1,3))
    A,B,C=tm(a),tm(b),tm(c)
    score=np.minimum(A,B)-C
    if score.max()>12: print(i, round(i/30,3), round(float(score.max()),1), np.unravel_index(score.argmax(),score.shape))

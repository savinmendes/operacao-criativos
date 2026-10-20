import subprocess,sys,numpy as np
for f in sys.argv[1:]:
    a=np.frombuffer(subprocess.check_output(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"]),np.float32)
    s=len(a)//16000; r=[20*np.log10(np.sqrt(np.mean(a[i*16000:(i+1)*16000]**2))+1e-9) for i in range(s)]
    print(f, " ".join(f"{x:.0f}" for x in r))

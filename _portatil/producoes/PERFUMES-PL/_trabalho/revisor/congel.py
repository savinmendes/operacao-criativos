import numpy as np,subprocess,sys
for n in sys.argv[1:]:
    W,H=90,160
    raw=subprocess.run(['ffmpeg','-v','error','-i',rf'C:\Users\PICHAU\Downloads\PERFUMES-PL\PARA-SUBIR\{n}.mp4','-vf',f'scale={W}:{H},crop={W}:90:0:20','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    f=np.frombuffer(raw,np.uint8).reshape(-1,90,W).astype(int)
    d=np.abs(np.diff(f,axis=0)).mean(axis=(1,2))
    # frozen runs
    runs=[];s=None
    for i,v in enumerate(d):
        if v<0.25:
            s=i if s is None else s
        else:
            if s is not None and i-s>=4: runs.append((round(s/30,2),round(i/30,2)))
            s=None
    # isolated single-frame spikes: big diff to prev and next but prev->next small (quadro solto)
    solto=[]
    for i in range(1,len(f)-1):
        a=np.abs(f[i]-f[i-1]).mean(); b=np.abs(f[i+1]-f[i]).mean(); c=np.abs(f[i+1]-f[i-1]).mean()
        if a>12 and b>12 and c<a*0.4: solto.append((round(i/30,2),round(a,1),round(c,1)))
    cuts=[round((i+1)/30,2) for i,v in enumerate(d) if v>25]
    print(n,'frames',len(f),'\n  congelado(>=4q):',runs,'\n  quadro solto:',solto,'\n  cortes:',cuts)

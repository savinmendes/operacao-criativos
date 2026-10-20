import sys, subprocess, numpy as np, cv2
for v in sys.argv[1:]:
    W,H=1080,1920
    p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
    i=0; on=[]; boxes=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        f=np.frombuffer(b,np.uint8).reshape(H,W,3)
        hsv=cv2.cvtColor(f[1500:1920],cv2.COLOR_BGR2HSV)
        m=(hsv[...,0]>15)&(hsv[...,0]<35)&(hsv[...,1]>150)&(hsv[...,2]>180)
        n=int(m.sum()); on.append(n)
        if n>3000:
            ys,xs=np.nonzero(m); boxes.append((i,ys.min()+1500,ys.max()+1500,xs.min(),xs.max()))
        i+=1
    on=np.array(on); act=on>3000
    idx=np.nonzero(act)[0]
    print('==',v.split('/')[-1],'frames',i,'arrow frames',len(idx), 'first',idx[0]/30 if len(idx) else None,'last',idx[-1]/30 if len(idx) else None)
    # runs
    runs=[];s=None
    for k in range(i):
        if act[k] and s is None: s=k
        if not act[k] and s is not None: runs.append((s/30,k/30)); s=None
    if s is not None: runs.append((s/30,i/30))
    print(' runs',[(round(a,2),round(b,2)) for a,b in runs])
    if boxes: 
        b=np.array(boxes); print(' y range',b[:,1].min(),b[:,2].max(),' x',b[:,3].min(),b[:,4].max())

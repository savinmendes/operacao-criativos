import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
out=[]
for q,f in enumerate(quadros(r"C:\Users\PICHAU\Downloads\TESTE1.mp4")):
    top=f[:160]; hsv=cv2.cvtColor(top,cv2.COLOR_BGR2HSV)
    m=((hsv[...,0]>=160)|(hsv[...,0]<=3))&(hsv[...,1]>120)&(hsv[...,2]>150)
    ys,xs=np.where(m)
    if len(xs)>300: out.append((q,xs.min(),ys.min(),xs.max(),ys.max(),len(xs)))
    else: out.append((q,-1,-1,-1,-1,len(xs)))
np.save("pill.npy",np.array(out))
# summarize runs
prev=None;st=None
for r in out+[(len(out),-1,-1,-1,-1,0)]:
    key=None if r[1]<0 else (r[1]//6,r[2]//6,r[3]//6,r[4]//6)
    if key!=prev:
        if prev is not None: print(f"{st/30:7.2f}-{r[0]/30:7.2f} q{st}-{r[0]-1} box {g[1:5]}")
        prev=key; st=r[0]; g=r

import sys, cv2, numpy as np
cap=cv2.VideoCapture(sys.argv[1]); N=int(float(sys.argv[2])*24)
H=np.zeros(1280); R=np.zeros(1280); X=[]
for i in range(0,N,12):
    cap.set(cv2.CAP_PROP_POS_FRAMES,i); ok,f=cap.read()
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    y=((h>=20)&(h<=38)&(s>=120)&(v>=170)); H+=y.sum(1)
    b,g,r=cv2.split(f.astype(int)); red=(r>160)&(g<70)&(b<70); R+=red.sum(1)
def rng(a,thr):
    idx=np.where(a>thr)[0]; return (idx.min(),idx.max()) if len(idx) else None
print("amarelo linhas", rng(H,H.max()*0.05), "vermelho", rng(R,R.max()*0.05))
for y0 in range(0,1280,40): print(y0, int(H[y0:y0+40].sum()), int(R[y0:y0+40].sum()))

import sys, cv2, numpy as np
src,ini,fim,step,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
cols=int(sys.argv[6]) if len(sys.argv)>6 else 12
cap=cv2.VideoCapture(src); fps=cap.get(5); ims=[]
t=ini
while t<=fim+1e-6:
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(round(t*fps))); ok,f=cap.read()
    if not ok: break
    f=cv2.resize(f,(144,256)); cv2.putText(f,f"{t:.2f}",(3,16),0,0.5,(0,0,0),3); cv2.putText(f,f"{t:.2f}",(3,16),0,0.5,(255,255,255),1); ims.append(f); t+=step
while len(ims)%cols: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out,cv2.vconcat([cv2.hconcat(ims[i:i+cols]) for i in range(0,len(ims),cols)]))

import cv2,numpy as np,sys
cap=cv2.VideoCapture("tratado.mp4")
for w in sys.argv[1:]:
    a,b=map(float,w.split(":")); cap.set(1,int(round(a*30))); prev=None; out=[]
    for i in range(int(round(a*30)),int(round(b*30))):
        ok,f=cap.read(); g=f[880:1100]; m=((g.min(axis=2)>225)).astype(np.uint8)  # caixa branca
        if prev is not None:
            d=(m!=prev).mean()
            if d>0.02: out.append(f"{i/30:.2f}({d:.2f})")
        prev=m
    print(w,":"," ".join(out))

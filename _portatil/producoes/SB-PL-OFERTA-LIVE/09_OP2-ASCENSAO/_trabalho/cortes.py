import cv2, numpy as np, sys
cap=cv2.VideoCapture(sys.argv[1]); prev=None; i=0; fps=cap.get(5)
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(108,192))[:120].astype(float)
    if prev is not None:
        d=np.abs(g-prev).mean()
        if d>6: print(f"{i/fps:.3f} f{i} diff={d:.1f}")
    prev=g; i+=1

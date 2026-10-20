import cv2, numpy as np, glob
def feat(f): return cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(36,64))[:40].astype(float)
cap=cv2.VideoCapture(r"..\..\SB-OP2-ASCENSAO.mp4")
alvos={"mulher_reza":8.1,"jesus_bau":10.5,"monges":14.5,"casa":18.0,"mulher_cel":24.0}
F={}
for k,t in alvos.items():
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read(); F[k]=feat(f)
res={k:[] for k in alvos}
for p in glob.glob(r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS\*.mp4"):
    c=cv2.VideoCapture(p); n=int(c.get(7)); fps=c.get(5)
    for i in range(0,n,int(fps/4) or 1):
        c.set(1,i); ok,f=c.read()
        if not ok: break
        g=feat(f)
        for k in alvos:
            res[k].append((np.abs(g-F[k]).mean(),p.split("\\")[-1],round(i/fps,2)))
for k in alvos:
    print(k, sorted(res[k])[:3])

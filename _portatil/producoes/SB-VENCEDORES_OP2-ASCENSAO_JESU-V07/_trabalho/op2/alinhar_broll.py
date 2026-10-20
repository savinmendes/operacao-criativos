import cv2, numpy as np
B=r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS\\"
def feat(f): return cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(54,96))[:60].astype(float)
def frames(p):
    c=cv2.VideoCapture(p); out=[]
    while True:
        ok,f=c.read()
        if not ok: break
        out.append(feat(f))
    return out,c.get(5)
ad,fa=frames(r"..\..\SB-OP2-ASCENSAO.mp4")
cenas=[("SB-BRV-55 MANO EN EL PECHO KLING25.mp4",7.2,9.0),("SB-BRV-01 REGALO NOMBRE KLING25.mp4",8.8,12.7),("SB-BRV-69 CATACUMBAS KLING25.mp4",12.4,16.6),("SB-BRV-03 LLUVIA MILAGROS KLING25.mp4",16.3,19.6),("SB-BRV-30 SCROLL DETENIDO KLING25.mp4",22.4,26.0)]
for f,a,b in cenas:
    br,fb=frames(B+f)
    print(f)
    for i in range(int(a*fa),int(b*fa),3):
        d=[np.abs(ad[i]-x).mean() for x in br]; j=int(np.argmin(d))
        print(f"  ad {i/fa:.2f} -> br {j/fb:.2f} d={d[j]:.1f}")

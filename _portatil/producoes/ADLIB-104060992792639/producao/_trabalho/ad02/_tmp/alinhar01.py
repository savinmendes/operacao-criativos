import cv2, numpy as np
def th(p):
    cap=cv2.VideoCapture(p); o=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        o.append(cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(36,64),interpolation=cv2.INTER_AREA).astype(np.float32))
    return np.array(o)
R=r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\UNICOS_HD"
a=th(R+r"\01.mp4"); b=th(R+r"\02.mp4")
np.save("t01.npy",a); np.save("t02.npy",b)
print(len(a),len(b))
# for frames of 02 sampled, find best match in 01
for k in range(0,len(b),60):
    d=np.abs(a-b[k]).mean(axis=(1,2)); j=int(d.argmin()); print(k, round(k/30,2), j, round(j/30,2), k-j, round(float(d[j]),2))

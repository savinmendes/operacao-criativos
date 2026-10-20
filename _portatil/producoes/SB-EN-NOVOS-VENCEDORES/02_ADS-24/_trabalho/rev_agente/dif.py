import cv2,numpy as np,json
cap=cv2.VideoCapture('../../SB-EN-ADS-24.mp4')
prev=None;d=[];dseam=[];i=0
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None:
        d.append((i/30, np.abs(g[100:760]-prev[100:760]).mean(), np.abs(g[200:380,330:480]-prev[200:380,330:480]).mean(), np.abs(g[760:880]-prev[760:880]).mean()))
    prev=g;i+=1
d=np.array(d); np.save('dif.npy',d)
med=np.median(d[:,1:],axis=0)
print('median',med)
ch=json.load(open('../chunks.json')); bounds=sorted(set([round(c[1],2) for c in ch]+[round(c[2],2) for c in ch]))
for t,a,b,c in d:
    if a>4*med[0] or b>4*med[1] or c>4*med[2]:
        near=[x for x in bounds if abs(x-t)<0.05]
        print(f"{t:7.2f} full{a:6.1f} face{b:6.1f} seam{c:6.1f} {'<-chunk '+str(near) if near else ''}")

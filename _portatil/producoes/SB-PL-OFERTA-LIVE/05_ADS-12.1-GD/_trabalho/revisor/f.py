import cv2,numpy as np
v=cv2.VideoCapture("../../SB-PL-ADS-12.1-GD.mp4")
fr=[]
while True:
    ok,f=v.read()
    if not ok: break
    fr.append(f)
print(len(fr))
def at(t): return fr[min(int(round(t*30)),len(fr)-1)]
def sheet(ts,crop,name,scale=0.5,cols=4):
    ims=[]
    for t in ts:
        y0,y1,x0,x1=crop; im=at(t)[y0:y1,x0:x1].copy()
        im=cv2.resize(im,None,fx=scale,fy=scale)
        cv2.putText(im,f"{t:.2f}",(5,25),0,0.8,(0,255,0),2); ims.append(im)
    while len(ims)%cols: ims.append(np.zeros_like(ims[0]))
    rows=[np.hstack(ims[i:i+cols]) for i in range(0,len(ims),cols)]
    cv2.imwrite(name,np.vstack(rows))
# subtitles
ts=[0.3,1.0,1.9,2.6,3.1,3.8,4.4,6.3,6.8,7.5,8.6,10.3,10.8,12.2,12.8,13.1,14.6,15.4,16.5,17.2,18.3,18.9,19.8,20.5,22.8,23.3,24.2,25.8,26.5,27.0,27.7,28.1,28.5,29.2,29.6,30.2,30.6,31.3]
sheet(ts[:20],(1050,1650,0,1080),"leg1.jpg",0.45)
sheet(ts[20:],(1050,1650,0,1080),"leg2.jpg",0.45)
sheet([0.1,0.8,1.6,2.4,3.2,4.0,4.6,4.95],(680,1000,880,1520),"carimbo.jpg",1.0) if False else None
sheet([0.1,0.8,1.6,2.4,3.2,4.0,4.6,4.95],(600,1100,780,1620) if False else (600,1100,0,1080),"carimbo.jpg",0.8)
# full overview at pause times
sheet([0.0,0.2,0.4,4.7,4.9,5.07,5.5,28.9,29.05,29.2,30.85,31.2,31.5],(0,1920,0,1080),"pausas_full.jpg",0.3,cols=5)
np.save("dummy.npy",np.array([0]))
# frame diffs for flashes
d=[float(np.mean(cv2.absdiff(fr[i],fr[i-1]))) for i in range(1,len(fr))]
m=[float(np.mean(f)) for f in fr]
for i in range(1,len(fr)-1):
    if d[i-1]>25 or (abs(m[i]-m[i-1])>15 and abs(m[i]-m[i+1])>15):
        print(f"t={i/30:.2f} diff={d[i-1]:.1f} luma {m[i-1]:.0f}->{m[i]:.0f}->{m[i+1]:.0f}")

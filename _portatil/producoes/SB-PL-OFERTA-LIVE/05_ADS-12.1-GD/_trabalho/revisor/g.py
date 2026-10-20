import cv2,numpy as np
def load(p):
    v=cv2.VideoCapture(p); fr=[]
    while True:
        ok,f=v.read()
        if not ok: break
        fr.append(f)
    return fr
pl=load("../../SB-PL-ADS-12.1-GD.mp4")
it=load(r"C:/Users/PICHAU/Downloads/SB-IT-OFERTA-LIVE/05_ADS-12.1-GD/SB-IT-ADS-12.1-GD.mp4")
print(len(it), it[0].shape)
def at(fr,t): return fr[min(int(round(t*30)),len(fr)-1)]
# stamp compare
a=at(pl,1.0)[540:720,620:1080]; b=at(it,1.0)[540:720,620:1080]
cv2.imwrite("carimbo_pl_vs_it.jpg",cv2.resize(np.vstack([a,b]),None,fx=2,fy=2))
# mouth crops
def strip(fr,ts,box,name):
    y0,y1,x0,x1=box; ims=[]
    for t in ts:
        im=cv2.resize(at(fr,t)[y0:y1,x0:x1],None,fx=1.5,fy=1.5); cv2.putText(im,f"{t:.2f}",(3,18),0,0.55,(0,255,0),2); ims.append(im)
    cv2.imwrite(name,np.hstack(ims))
strip(pl,[0.0,0.07,0.13,0.2,0.27,0.33,0.4,0.5,4.6,4.7,4.8,4.9,5.0],(1050,1250,760,960),"boca_gancho.jpg")
strip(pl,[5.07,5.2,5.3,5.44,28.7,28.8,28.9,29.0,29.1,29.2,29.3],(430,630,420,660),"boca_cta1.jpg")
strip(pl,[30.7,30.8,30.85,30.95,31.05,31.15,31.25,31.35,31.45,31.55],(430,630,420,660),"boca_fim.jpg")

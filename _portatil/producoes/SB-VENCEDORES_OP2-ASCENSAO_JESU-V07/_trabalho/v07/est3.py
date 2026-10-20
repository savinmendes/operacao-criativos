import cv2,numpy as np
def rd(p,k):
    c=cv2.VideoCapture(p); c.set(1,k); ok,f=c.read(); return cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
SC=0.25
for src,fps,ts,guess in [('src_corpo_cta.mp4',25,[6.3,6.5,9.9,15.7,19.0,25.8,28.5],-6.1)]:
  for t in ts:
    e=rd('es.mp4',round(t*30)); e=cv2.resize(e,(720,1280))[60:750]
    best=(-1,)
    for dt in np.arange(-0.3,0.31,0.04):
      k=round((t+guess+dt)*fps)
      if k<0 or k>670: continue
      s_img=cv2.resize(rd(src,k),None,fx=SC*1080/720 if False else SC,fy=SC)
      for s in np.arange(1.0,1.2,0.02):
        tpl=cv2.resize(e,None,fx=SC/s,fy=SC/s)
        r=cv2.matchTemplate(s_img,tpl,cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(r)
        if mv>best[0]: best=(mv,k,s,ml)
    mv,k,s,ml=best
    print(src,t,'srcT=%.2f scale=%.2f r=%.3f'%(k/fps,s,mv))

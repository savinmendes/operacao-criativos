import cv2,numpy as np
def es_at(t):
    c=cv2.VideoCapture('es.mp4'); c.set(1,round(t*30)); ok,f=c.read(); return cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
def src_at(p,k):
    c=cv2.VideoCapture(p); c.set(1,k); ok,f=c.read(); return cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
SC=0.25
for src,ts in [('br23',[10.45,11.0,11.6]),('br29',[12.0,13.6,15.3]),('br20',[19.5,20.8,22.0]),('br07',[22.4,23.9,25.3]),('br02',[29.0,31.0,33.0])]:
  for t in ts:
    e=es_at(t)[100:1150]  # top region of ES frame, avoid caption
    best=(-1,)
    for k in range(0,121,8):
      s_img=cv2.resize(src_at(src+'.mp4',k),None,fx=SC,fy=SC)
      for s in np.arange(1.0,1.5,0.02):
        tpl=cv2.resize(e,None,fx=SC/s,fy=SC/s)
        r=cv2.matchTemplate(s_img,tpl,cv2.TM_CCOEFF_NORMED); _,mv,_,ml=cv2.minMaxLoc(r)
        if mv>best[0]: best=(mv,k,s,ml)
    mv,k,s,ml=best
    # ES pixel (0,100) maps to source (ml/SC); crop origin in source:
    x0=ml[0]/SC; y0=ml[1]/SC-100/s
    print(src,t,'k=%d tsrc=%.2f scale=%.2f x0=%.0f y0=%.0f r=%.3f'%(k,k/24,s,x0,y0,mv))

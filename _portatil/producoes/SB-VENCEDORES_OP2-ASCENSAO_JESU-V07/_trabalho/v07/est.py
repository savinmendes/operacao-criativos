import cv2,numpy as np
W,H=108,192
def es_at(t):
    c=cv2.VideoCapture('es.mp4'); c.set(1,round(t*30)); ok,f=c.read(); return cv2.resize(f,(W,H)).astype(float)
def frames(p):
    c=cv2.VideoCapture(p); out=[]
    while True:
        ok,f=c.read()
        if not ok: break
        out.append(f)
    return out
mask=np.ones((H,W),bool); mask[int(.66*H):int(.95*H)]=False
def crop(f,s):
    h,w=f.shape[:2]; cw,ch=w/s,h/s; x0=(w-cw)/2; y0=(h-ch)/2
    return cv2.resize(f[int(y0):int(y0+ch),int(x0):int(x0+cw)],(W,H)).astype(float)
for src,a,b in [('br23',10.4,11.65),('br29',11.95,15.3),('br20',19.45,22.05),('br07',22.35,25.35),('br02',28.95,33.0)]:
    fs=frames(src+'.mp4')
    for t in (a,b):
        e=es_at(t); best=(1e9,)
        for k in range(0,len(fs),2):
            for s in np.arange(1.0,1.45,0.025):
                d=np.abs(crop(fs[k],s)-e)[mask].mean()
                if d<best[0]: best=(d,k,s)
        print(src,t,'frame',best[1],'t_src=%.2f'%(best[1]/24),'scale=%.3f'%best[2],'d=%.1f'%best[0])

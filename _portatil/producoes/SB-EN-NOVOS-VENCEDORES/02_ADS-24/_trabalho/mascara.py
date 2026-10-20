import cv2, numpy as np
Y0,Y1=860,1190
def mascara(f, hook=False, setas=False):
    H,W=f.shape[:2]
    full=np.zeros((H,W),np.uint8)
    roi=f[Y0:Y1]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=[hsv[...,i].astype(int) for i in range(3)]
    if hook:
        wht=((s<=30)&(v>=225)).astype(np.uint8)
        wht=cv2.morphologyEx(wht,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(wht)
        m=np.zeros_like(wht)
        for k in range(1,n):
            x,y,w,hh,a=st[k]
            if 25<=hh<=140 and w>=60 and a>=0.6*w*hh*0.5:
                m[max(0,y-6):y+hh+6,max(0,x-6):x+w+6]=1
        full[Y0:Y1]=m; return full
    yel=(h>=18)&(h<=40)&(s>=110)&(v>=170)
    red=((h<=8)|(h>=170))&(s>=140)&(v>=150)
    grn=(h>=42)&(h<=85)&(s>=110)&(v>=120)
    wht=(s<=30)&(v>=225)
    dark=(v<=70).astype(np.uint8)
    nd=cv2.dilate(dark,np.ones((7,7),np.uint8))>0
    cand=((yel|red|grn|wht)&nd).astype(np.uint8)
    cand=cv2.morphologyEx(cand,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    grp=cv2.dilate(cand,cv2.getStructuringElement(cv2.MORPH_RECT,(31,11)))
    n,lab,st,_=cv2.connectedComponentsWithStats(grp)
    m=np.zeros_like(cand)
    for k in range(1,n):
        x,y,w,hh,a=st[k]
        sub=cand*(lab==k); cnt=int(sub.sum())
        if 22<=hh<=260 and w>=30 and cnt>=150:
            ys,xs=np.where(sub>0); P=10
            m[max(0,ys.min()-P):ys.max()+P+4,max(0,xs.min()-P):xs.max()+P]=1
    full[Y0:Y1]=m
    if setas:
        hs=cv2.cvtColor(f[980:],cv2.COLOR_BGR2HSV); hh_,ss,vv=[hs[...,i].astype(int) for i in range(3)]
        r=(((hh_<=10)|(hh_>=165))&(ss>=120)&(vv>=120)).astype(np.uint8)
        r=cv2.morphologyEx(r,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(r)
        mm=np.zeros_like(r)
        for k in range(1,n):
            if st[k][4]>=300: mm|=(lab==k).astype(np.uint8)
        mm=cv2.dilate(mm,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
        full[980:]|=mm
    return full
if __name__=="__main__":
    import sys
    vis=[]
    for p in sys.argv[1:]:
        t=float(p.split('_')[-1][:-4]); f=cv2.imread(p); m=mascara(f,hook=t<4.25,setas=129<t<136)
        o=f.copy(); o[m>0]=(0.4*o[m>0]+[0,0,150]).astype(np.uint8); vis.append(cv2.resize(o[820:1280],(270,173)))
    while len(vis)%4: vis.append(np.zeros_like(vis[0]))
    cv2.imwrite('q/mask_vis.jpg',cv2.vconcat([cv2.hconcat(vis[i:i+4]) for i in range(0,len(vis),4)]))

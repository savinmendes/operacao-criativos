import cv2, numpy as np
Y0,Y1=780,1160
def mascara(f, hook=False):
    roi=f[Y0:Y1]; hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    yel=((h>=18)&(h<=40)&(s>=90)&(v>=150)).astype(np.uint8)
    wht=((s<=(15 if hook else 28))&(v>=(240 if hook else 222))).astype(np.uint8)
    dark=((v<=85)).astype(np.uint8)
    if hook:
        fill=yel|wht; cand=fill
    else:
        nd=cv2.dilate(dark,np.ones((9,9),np.uint8))
        fill=(yel|wht)&nd
        cand=fill
    cand=cv2.morphologyEx(cand,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    # agrupa em linha de texto
    grp=cv2.dilate(cand,cv2.getStructuringElement(cv2.MORPH_RECT,(31,9)))
    n,lab,st,_=cv2.connectedComponentsWithStats(grp)
    m=np.zeros_like(cand)
    for k in range(1,n):
        x,y,w,hh,a=st[k]
        sub=cand*(lab==k)
        cnt=int(sub.sum())
        if hh>=18 and w>=40 and cnt>=150 and hh<=300:
            if hook:
                m|=cv2.dilate(sub,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
            else:
                ys,xs=np.where(sub>0); P=12
                m[max(0,ys.min()-P):ys.max()+P+4,max(0,xs.min()-P):xs.max()+P]=1
    full=np.zeros(f.shape[:2],np.uint8); full[Y0:Y1]=m; return full
if __name__=="__main__":
    import sys
    vis=[]
    for p in sys.argv[1:]:
        f=cv2.imread(p); m=mascara(f, hook=float(p[2:-4])<4.3)
        o=f.copy(); o[m>0]=(0.5*o[m>0]+[0,0,127]).astype(np.uint8); vis.append(cv2.resize(o[700:1200],(360,250)))
    cv2.imwrite('mask_vis.jpg',cv2.vconcat([cv2.hconcat(vis[:5]),cv2.hconcat(vis[5:10])]))

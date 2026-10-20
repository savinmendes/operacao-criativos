import cv2,numpy as np
cap=cv2.VideoCapture('../../../UNICOS_HD/11.mp4')
Y0,Y1=836,980
cov={}
shots=[(0,265),(271,359),(462,936),(1138,1861)]
i=0; boxes=[]
while True:
    ok,f=cap.read()
    if not ok: break
    roi=f[Y0:Y1]
    b,g,r=cv2.split(roi.astype(np.int16)); gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    txt=((np.minimum(r,g)>165)&(gray>165)).astype(np.uint8)&cv2.dilate((gray<70).astype(np.uint8),np.ones((7,7),np.uint8))
    m=np.zeros(gray.shape,np.uint8)
    for ya,yb in [(0,72),(72,144)]:
        ys,xs=np.nonzero(txt[ya:yb])
        if len(xs)>60:
            x0,x1=np.percentile(xs,0.5),np.percentile(xs,99.5)
            yy0,yy1=np.percentile(ys,0.5)+ya,np.percentile(ys,99.5)+ya
            m[max(0,int(yy0)-8):int(yy1)+10, max(0,int(x0)-10):int(x1)+12]=1
    boxes.append(m); i+=1
np.save('_tmp/boxmasks.npy',np.stack(boxes))
for a,b in shots:
    M=np.stack(boxes[a:b]); free=(M==0).any(0)
    print(a,b,'holes',int((~free).sum()), 'rows', np.nonzero((~free).any(1))[0][[0,-1]] if (~free).any() else None, 'cols', np.nonzero((~free).any(0))[0][[0,-1]] if (~free).any() else None)

import cv2, numpy as np, sys
def grab(p, idxs):
    cap=cv2.VideoCapture(p); out={}; i=0; s=set(idxs); m=max(idxs)
    while i<=m:
        ok,f=cap.read()
        if not ok: break
        if i in s: out[i]=f
        i+=1
    return out
def strip(p, centers, outname, before=5, after=4, w=216, h=384):
    idx=[c+k for c in centers for k in range(-before,after+1)]
    fr=grab(p,idx); rows=[]
    for c in centers:
        tiles=[]
        for k in range(-before,after+1):
            t=cv2.resize(fr[c+k],(w,h)); cv2.putText(t,str(c+k),(5,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2); tiles.append(t)
        rows.append(np.hstack(tiles))
    cv2.imwrite(outname,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,85])
if __name__=='__main__':
    p=sys.argv[1]; out=sys.argv[2]; cs=[int(x) for x in sys.argv[3].split(',')]
    strip(p,cs,out)

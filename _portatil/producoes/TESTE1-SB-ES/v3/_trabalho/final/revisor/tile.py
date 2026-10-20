import cv2,numpy as np,sys
def tile(frames,cols,w,out,lab=True):
    h=int(w*16/9);rows=(len(frames)+cols-1)//cols
    can=np.zeros((rows*h,cols*w,3),np.uint8)
    for k,i in enumerate(frames):
        if i is None: continue
        im=cv2.resize(cv2.imread(f'f/{i:05d}.jpg'),(w,h))
        if lab: cv2.putText(im,f'{i} {i/30:.2f}',(3,14),0,0.42,(0,255,255),1)
        r,c=divmod(k,cols);can[r*h:(r+1)*h,c*w:(c+1)*w]=im
    cv2.imwrite(out,can)
if __name__=='__main__':
    a=int(sys.argv[1]);n=int(sys.argv[2]);cols=int(sys.argv[3]);w=int(sys.argv[4]);out=sys.argv[5]
    tile(list(range(a,a+n)),cols,w,out)

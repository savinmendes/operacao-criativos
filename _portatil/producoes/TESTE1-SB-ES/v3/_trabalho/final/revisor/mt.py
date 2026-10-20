import cv2,numpy as np,sys
def mtile(frames,cols,w,out):
    ims=[]
    for i in frames:
        im=cv2.imread(f'm/{i:05d}.jpg')
        h=int(im.shape[0]*w/im.shape[1]);im=cv2.resize(im,(w,h))
        cv2.putText(im,f'{i} {i/30:.2f}',(3,14),0,0.45,(0,255,255),1);ims.append(im)
    h=max(x.shape[0] for x in ims);rows=(len(ims)+cols-1)//cols
    can=np.zeros((rows*h,cols*w,3),np.uint8)
    for k,im in enumerate(ims):
        r,c=divmod(k,cols);can[r*h:r*h+im.shape[0],c*w:(c+1)*w]=im
    cv2.imwrite(out,can)
if __name__=='__main__':
    fr=[]
    for a in sys.argv[3].split(','):
        s,n=a.split(':');fr+=list(range(int(s),int(s)+int(n)))
    mtile(fr,int(sys.argv[2]),int(sys.argv[4]) if len(sys.argv)>4 else 160,sys.argv[1])

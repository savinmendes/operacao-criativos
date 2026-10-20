import cv2,numpy as np,warnings
warnings.filterwarnings("ignore")
BM=np.load('_tmp/boxmasks.npy'); Y0,Y1=836,980
pl=cv2.imread('_tmp/placas.png'); PC=pl[144:288].astype(np.float32); PE=pl[288:432].astype(np.float32)
c=cv2.VideoCapture('../../../UNICOS_HD/11.mp4'); sc=[]
for i in range(1861):
    ok,f=c.read()
    if not((271<=i<=358) or (462<=i<=935) or i>=1138): sc.append(-1); continue
    P=PE if i>=1138 else PC
    roi=f[Y0:Y1].astype(np.float32); m=cv2.dilate(BM[i].astype(np.uint8),np.ones((9,9),np.uint8))
    d=np.abs(roi-P).mean(2); d[m>0]=0
    # pior bloco 40px de coluna, só pixels livres
    free=(m==0).astype(float)
    cols=[d[:,x:x+40].sum()/max(1,free[:,x:x+40].sum()) for x in range(0,720,40)]
    sc.append(max(cols))
sc=np.array(sc); np.save('_tmp/mov.npy',sc)
w=sc>=0
for thr in [10,15,20,25,30]: print(thr,(sc[w]>thr).sum())
for i in range(0,1861,30):
    if sc[i]>=0: print(round(i/30,1),round(sc[i],1),end=' | ')

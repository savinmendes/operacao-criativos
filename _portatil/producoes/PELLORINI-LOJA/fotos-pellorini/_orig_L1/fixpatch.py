# uso: python fixpatch.py <chave> cx,cy,rx,ry [cx,cy,rx,ry ...]  -> cola o original nessas elipses (alinhado + cor)
import sys,numpy as np,cv2,shutil,os
from PIL import Image
D=r"C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini"
k=sys.argv[1]
gen_path=rf"{D}\{k}.jpg"; bak=rf"{D}\_orig_L1\{k}_gen.png"
if not os.path.exists(bak): Image.open(gen_path).save(bak)
o=cv2.imread(rf"{D}\_orig_L1\{k}.jpg"); g=cv2.imread(bak); out=g.astype(np.float32)
for spec in sys.argv[2:]:
    cx,cy,rx,ry=map(int,spec.split(','))
    w=max(rx,ry)*3; x0,y0,x1,y1=cx-w,cy-w,cx+w,cy+w
    a=cv2.cvtColor(o[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32); b=cv2.cvtColor(g[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
    win=cv2.createHanningWindow(a.shape[::-1],cv2.CV_32F)
    (dx,dy),resp=cv2.phaseCorrelate(a,b,win)
    M=np.float32([[1,0,dx],[0,1,dy]]); os_=cv2.warpAffine(o,M,(o.shape[1],o.shape[0]),borderMode=cv2.BORDER_REFLECT)
    c=(int(round(cx+dx)),int(round(cy+dy)))
    mask=np.zeros(o.shape[:2],np.float32); cv2.ellipse(mask,c,(rx,ry),0,0,360,1,-1)
    mask=cv2.GaussianBlur(mask,(0,0),max(3,min(rx,ry)/5))[...,None]
    ring=np.zeros(o.shape[:2],np.uint8); cv2.ellipse(ring,c,(rx+20,ry+20),0,0,360,1,-1); cv2.ellipse(ring,c,(rx+5,ry+5),0,0,360,0,-1)
    r=ring.astype(bool); gain=g[r].mean(0)/np.maximum(os_[r].mean(0),1)
    osc=np.clip(os_.astype(np.float32)*gain,0,255)
    out=osc*mask+out*(1-mask)
    print(k,spec,'shift',round(dx,1),round(dy,1),'resp',round(resp,2),'gain',np.round(gain,3))
Image.fromarray(cv2.cvtColor(out.clip(0,255).astype(np.uint8),cv2.COLOR_BGR2RGB)).save(gen_path,quality=94)

import numpy as np,cv2,sys
from PIL import Image
# name: (cx,cy,rx,ry)
D={'pellorini-clovera_1':(1577,1236,85,85),'pellorini-clovera_6':(997,1373,105,105),'pellorini-fiorella_1':(1526,1191,80,75),
'pellorini-grazia_3':(1075,1097,85,95),'pellorini-luna-perla_1':(1558,1220,75,95),'pellorini-lunetta_1':(1502,1157,55,85),
'pellorini-serafina_1':(1592,1148,125,115),'pellorini-valore_2':(1014,1268,120,160)}
only=sys.argv[1:] or list(D)
for n in only:
  cx,cy,rx,ry=D[n]
  o=cv2.imread(n+'.png');g=cv2.imread(n+'_gen.png')
  x0,y0,x1,y1=cx-300,cy-300,cx+300,cy+300
  a=cv2.cvtColor(o[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
  b=cv2.cvtColor(g[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
  (dx,dy),resp=cv2.phaseCorrelate(a,b)
  # shift original by (dx,dy) to align with gen
  M=np.float32([[1,0,dx],[0,1,dy]])
  os_=cv2.warpAffine(o,M,(o.shape[1],o.shape[0]),borderMode=cv2.BORDER_REFLECT)
  mask=np.zeros(o.shape[:2],np.float32)
  cv2.ellipse(mask,(int(cx+dx),int(cy+dy)),(rx,ry),0,0,360,1,-1)
  mask=cv2.GaussianBlur(mask,(0,0),8)[...,None]
  # color match: ring around ellipse
  ring=np.zeros(o.shape[:2],np.uint8);cv2.ellipse(ring,(int(cx+dx),int(cy+dy)),(rx+40,ry+40),0,0,360,1,-1);cv2.ellipse(ring,(int(cx+dx),int(cy+dy)),(rx+15,ry+15),0,0,360,0,-1)
  r=ring.astype(bool);gain=g[r].mean(0)/np.maximum(os_[r].mean(0),1)
  osc=np.clip(os_.astype(np.float32)*gain,0,255)
  out=(osc*mask+g.astype(np.float32)*(1-mask)).astype(np.uint8)
  cv2.imwrite(n+'_fix.png',out)
  print(n,'shift',round(dx,2),round(dy,2),'resp',round(resp,3),'gain',np.round(gain,3))

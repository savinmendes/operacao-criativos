import cv2,numpy as np,sys
C={'pellorini-marcello_2':(998,1050),'pellorini-cristallo_2':(1126,973),'pellorini-cristallo_3':(1050,742),'pellorini-dario_1':(1024,1254),
'pellorini-dario_3':(1321,1152),'pellorini-roma_1':(1050,1101),'pellorini-roma_2':(538,1178),'pellorini-roma_3':(1213,1024),
'pellorini-milano-iced_1':(998,1075),'pellorini-milano-iced_2':(604,922),'pellorini-milano-iced_3':(1316,1178)}
R=int(sys.argv[1]) if len(sys.argv)>1 else 150
for n,(cx,cy) in C.items():
  o=cv2.imread(f'_orig_L4/{n}.png');o=cv2.resize(o,(2048,2048),interpolation=cv2.INTER_AREA)
  g=cv2.imread(f'{n}.jpg')
  x0,y0,x1,y1=cx-300,cy-300,cx+300,cy+300
  a=cv2.cvtColor(o[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32);b=cv2.cvtColor(g[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
  (dx,dy),resp=cv2.phaseCorrelate(a,b)
  M=np.float32([[1,0,dx],[0,1,dy]]);os_=cv2.warpAffine(o,M,(2048,2048),borderMode=cv2.BORDER_REFLECT)
  ca=os_[cy-R:cy+R,cx-R:cx+R];cb=g[cy-R:cy+R,cx-R:cx+R]
  diff=np.abs(ca.astype(int)-cb.astype(int)).mean()
  z=lambda im:cv2.resize(im,None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC)
  cv2.imwrite(f'_orig_L4/z_{n}.jpg',np.hstack([z(ca),np.full((6*R,10,3),255,np.uint8),z(cb)]),[cv2.IMWRITE_JPEG_QUALITY,88])
  print(n,'shift',round(dx,2),round(dy,2),'resp',round(resp,3),'diff',round(diff,2))

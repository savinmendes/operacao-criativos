# cola o mostrador original (alinhado, borda suave, ajuste de cor) sobre a foto final; metodo de _orig_L3/fixdial.py
import numpy as np,cv2,sys,os,shutil
# ('e',cx,cy,rx,ry) elipse | ('r',x0,y0,x1,y1) retangulo arredondado  (coords na foto final 2048)
D={'pellorini-marcello_2':('e',1035,1057,110,110),
'pellorini-cristallo_2':('r',1058,878,1222,1038),
'pellorini-cristallo_3':('r',900,598,1120,850),
'pellorini-dario_1':('e',1039,1259,162,162),
'pellorini-dario_3':('e',1328,1164,107,107),
'pellorini-roma_1':('r',910,1001,1127,1213),
'pellorini-roma_2':('r',436,1008,670,1218),
'pellorini-roma_3':('r',1133,959,1300,1103),
'pellorini-milano-iced_1':('e',1005,1042,122,110),
'pellorini-milano-iced_2':('e',621,900,122,120),
'pellorini-milano-iced_3':('e',1316,1130,105,92)}
only=sys.argv[1:] or list(D)
def shape(m,s,grow,val):
  if s[0]=='e': cv2.ellipse(m,(s[1],s[2]),(s[3]+grow,s[4]+grow),0,0,360,val,-1)
  else:
    x0,y0,x1,y1=s[1]-grow,s[2]-grow,s[3]+grow,s[4]+grow;r=max(12,int(0.12*min(x1-x0,y1-y0)))
    cv2.rectangle(m,(x0+r,y0),(x1-r,y1),val,-1);cv2.rectangle(m,(x0,y0+r),(x1,y1-r),val,-1)
    for cx,cy in [(x0+r,y0+r),(x1-r,y0+r),(x0+r,y1-r),(x1-r,y1-r)]: cv2.circle(m,(cx,cy),r,val,-1)
for n in only:
  s=D[n];bk=f'_orig_L4/{n}_antes.jpg'
  if not os.path.exists(bk): shutil.copy2(f'{n}.jpg',bk)
  g=cv2.imread(bk);o=cv2.imread(f'_orig_L4/{n}.png');o=cv2.resize(o,(g.shape[1],g.shape[0]),interpolation=cv2.INTER_AREA)
  if s[0]=='e': cx,cy=s[1],s[2]
  else: cx,cy=(s[1]+s[3])//2,(s[2]+s[4])//2
  x0,y0,x1,y1=cx-300,cy-300,cx+300,cy+300
  a=cv2.cvtColor(o[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32);b=cv2.cvtColor(g[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
  (dx,dy),resp=cv2.phaseCorrelate(a,b)
  M=np.float32([[1,0,dx],[0,1,dy]]);os_=cv2.warpAffine(o,M,(o.shape[1],o.shape[0]),borderMode=cv2.BORDER_REFLECT)
  mask=np.zeros(o.shape[:2],np.float32);shape(mask,s,0,1);mask=cv2.GaussianBlur(mask,(0,0),6)[...,None]
  ring=np.zeros(o.shape[:2],np.uint8);shape(ring,s,30,1);shape(ring,s,8,0);r=ring.astype(bool)
  gain=g[r].mean(0)/np.maximum(os_[r].mean(0),1)
  osc=np.clip(os_.astype(np.float32)*gain,0,255)
  out=(osc*mask+g.astype(np.float32)*(1-mask)).astype(np.uint8)
  cv2.imwrite(f'{n}.jpg',out,[cv2.IMWRITE_JPEG_QUALITY,94])
  # comparativo 3x: original | antes | depois
  R=(max(s[3],s[4])+20) if s[0]=='e' else max(s[3]-s[1],s[4]-s[2])//2+20
  def z(im): c=im[cy-R:cy+R,cx-R:cx+R];return cv2.resize(c,(600,600),interpolation=cv2.INTER_CUBIC)
  sep=np.full((600,8,3),255,np.uint8)
  cv2.imwrite(f'_orig_L4/cmp_{n}.jpg',np.hstack([z(os_),sep,z(g),sep,z(out)]),[cv2.IMWRITE_JPEG_QUALITY,88])
  print(n,'shift',round(dx,2),round(dy,2),'resp',round(resp,3),'gain',np.round(gain,3))

import cv2,numpy as np,sys
exec(open('_orig_L4/zoom.py').read().split('R=')[0])
R=220
for n,(cx,cy) in C.items():
  if len(sys.argv)>1 and n not in sys.argv[1:]: continue
  g=cv2.imread(f'{n}.jpg');x0,y0=cx-R,cy-R
  c=cv2.resize(g[y0:y0+2*R,x0:x0+2*R],None,fx=2,fy=2)
  for k in range(0,2*R+1,40):
    cv2.line(c,(2*k,0),(2*k,4*R),(0,255,0),1);cv2.line(c,(0,2*k),(4*R,2*k),(0,255,0),1)
    cv2.putText(c,str(x0+k),(2*k+2,14),0,0.4,(0,255,255),1);cv2.putText(c,str(y0+k),(2,2*k+14),0,0.4,(0,255,255),1)
  cv2.imwrite(f'_orig_L4/g_{n}.jpg',c,[cv2.IMWRITE_JPEG_QUALITY,85])

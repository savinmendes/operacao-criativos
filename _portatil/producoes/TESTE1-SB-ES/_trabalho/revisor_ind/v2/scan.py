import cv2,numpy as np,glob
fs=sorted(glob.glob('v2/f30/*.jpg')); N=len(fs)
# old refs
ref_hdr=cv2.imread('f30/00923.jpg')[140:230,150:720].astype(int)
ref_name=cv2.imread('f30/01787.jpg')[62:98,126:362].astype(int)
rows=[]
prev=None
for i,f in enumerate(fs):
  im=cv2.imread(f); 
  small=cv2.resize(im,(90,160)).astype(np.float32)
  diff=0 if prev is None else float(np.abs(small-prev).mean()); prev=small
  r=im[140:230,150:720].astype(int)
  hdr = np.abs(r-ref_hdr).mean() if (r>235).mean()>=0.7 else -1
  p=im[62:108,402:516].astype(int)
  pink=((p[:,:,2]>180)&(p[:,:,1]<90)&(p[:,:,0]>80)).mean()
  # name text: bright pixels in name region
  nr=cv2.cvtColor(im[62:98,126:362],cv2.COLOR_BGR2GRAY); name_white=(nr>225).mean()
  cr=cv2.cvtColor(im[1177:1206,63:283],cv2.COLOR_BGR2GRAY); com_white=(cr>200).mean()
  red=int(((im[150:1100,:,2]>190)&(im[150:1100,:,1]<60)&(im[150:1100,:,0]<60)).sum())
  g=cv2.cvtColor(im[0:20,592:706],cv2.COLOR_BGR2GRAY); seal=((g<110).mean()>=0.35 and (g>200).mean()>=0.05)
  rows.append((i,diff,hdr,pink,name_white,com_white,red,seal))
np.save('v2/scan.npy',np.array(rows,dtype=float))

import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
a=list(quadros(sys.argv[1],0,170)); b=list(quadros("src13.mp4",0,170))
idx=[int(x) for x in sys.argv[3].split(",")]
cr=lambda f: cv2.resize(f[800:960,450:620],None,fx=2,fy=2)
r1=np.hstack([cr(a[i]) for i in idx]); r2=np.hstack([cr(b[i]) for i in idx])
cv2.imwrite(sys.argv[2],np.vstack([r1,r2]))

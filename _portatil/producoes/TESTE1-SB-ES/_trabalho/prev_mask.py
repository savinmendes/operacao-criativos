import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
from mascaras import mascara
qs=[int(x) for x in sys.argv[1].split(",")]
ims=[]
for q in qs:
    f=next(quadros(r"C:\Users\PICHAU\Downloads\TESTE1.mp4",q,1)); m=mascara(f,q)
    o=f.copy(); o[m>0]=(0.5*o[m>0]+[0,0,127]).astype(np.uint8); ims.append(cv2.resize(o,(360,640)))
cv2.imwrite(sys.argv[2], np.hstack(ims))

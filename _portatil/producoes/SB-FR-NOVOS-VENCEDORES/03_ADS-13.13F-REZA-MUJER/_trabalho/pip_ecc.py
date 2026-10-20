import cv2,numpy as np,sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
SRC=r"C:\Users\PICHAU\Downloads\ADS 13\ADS 13.13F REZA-MUJER.mp4"; BASE=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama\base_limpa2.mp4"
A=list(quadros(SRC,0,175)); B=list(quadros(BASE,0,175))
g=lambda x: cv2.cvtColor(x,cv2.COLOR_BGR2GRAY).astype(np.float32)
for n in [10,50,100,140,170]:
    s=0.6; M=np.float32([[s,0,392-180*s],[0,s,774-150*s]])
    # ECC: warp base -> src, mascara na regiao do rosto no src
    mask=np.zeros((1280,720),np.uint8); mask[700:1050,380:680]=1
    Mi=cv2.invertAffineTransform(M).astype(np.float32)
    cc,W=cv2.findTransformECC(g(A[n]),g(B[n]),Mi,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,200,1e-6),mask,5)
    Wf=cv2.invertAffineTransform(W); print(n,round(cc,4),np.round(Wf,4).tolist())

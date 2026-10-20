import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
from mascaras import red_mask
for k,f in enumerate(quadros(r"C:\Users\PICHAU\Downloads\TESTE1.mp4",1893,323)):
    if k%3==0: print(1893+k, int(red_mask(f).sum()))

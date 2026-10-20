import sys,json,numpy as np,cv2
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho")
from comum3 import quadros
v=r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\SB-EN-AVATAR-REST_v2.mp4"
lum=[];dif=[];prev=None;small=[]
for i,f in enumerate(quadros(v,w=1080,h=1920)):
    s=cv2.resize(f,(135,240),interpolation=cv2.INTER_AREA)
    small.append(s)
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    # luma sem a faixa de legenda (exclui 1150-1650)
    lum.append(float(np.concatenate([g[:1150],g[1650:]]).mean()))
    if prev is not None: dif.append(float(np.abs(s.astype(int)-prev.astype(int)).mean()))
    else: dif.append(0.0)
    prev=s
np.save("small.npy",np.array(small))
json.dump({"lum":lum,"dif":dif},open("stats.json","w"))
print(len(lum))

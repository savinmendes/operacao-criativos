# Quadros 2030-2175 (legenda sobre o prédio): máscara em faixa de largura total, LaMa em meia resolução
import warnings; warnings.filterwarnings("ignore")
import subprocess, numpy as np, cv2
from teste_lama2 import limpar
from mascara2 import mascara
SRC=r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"; W,H=1080,1920; A,B=2030,2176
K=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,41))
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf",f"select='between(n,{A},{B-1})',scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-fps_mode","passthrough","-f","rawvideo","-"],stdout=subprocess.PIPE)
out=[]
for i in range(A,B):
    f=np.frombuffer(dec.stdout.read(W*H*3),np.uint8).reshape(H,W,3).copy()
    m=cv2.dilate(mascara(f),K); ys=np.where(m.any(1))[0]
    mb=np.zeros_like(m)
    if len(ys): mb[ys.min():ys.max()+1,:]=1
    else: mb[1400:1600,:]=1
    out.append(limpar(f,mb,0.5))
np.save("patch_v2.npy",np.stack(out)); print("ok",len(out))

"""LaMa (GPU) na legenda PT do 03 (branca/amarela, sem contorno). Mascara justa: pixels de texto (branco puro v>=246,s<35 ou amarelo)
nas faixas da legenda (y 968-1045; no split 1198-1436 tambem y 612-668; mao 'clique' 1750-1950 ate y 1135, x 250-480), fechados e dilatados 9 px.
Salva a regiao de contexto preenchida em _tmp/lama/NNNN.png (so quando ha mascara) e as mascaras em _tmp/mask/NNNN.png."""
import os, time, warnings, sys; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
os.makedirs('_tmp/lama',exist_ok=True); os.makedirs('_tmp/mask',exist_ok=True)
a0=int(sys.argv[1]) if len(sys.argv)>1 else 0; a1=int(sys.argv[2]) if len(sys.argv)>2 else 2893
lama=SimpleLama(); print("cuda",torch.cuda.is_available(),flush=True)
cap=cv2.VideoCapture('../../../UNICOS_HD/03.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES,a0); t0=time.time()
def txtmask(f):
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0].astype(int),hsv[...,1].astype(int),hsv[...,2].astype(int)
    return (((v>=246)&(s<35))|((h>=15)&(h<=42)&(s>=100)&(v>=200))).astype(np.uint8)
for i in range(a0,a1):
    ok,f=cap.read()
    if not ok: break
    t=txtmask(f); band=np.zeros_like(t); band[968:1045]=1
    if 1198<=i<=1436: band[612:668]=1
    if 1750<=i<=1950: band[1040:1135,250:480]=1
    m=t&band
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m)
    keep=np.zeros_like(m)
    for k in range(1,n):
        if st[k,4]>=6: keep[lab==k]=1
    m=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(19,19)))
    vv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)[1015:1150,270:470,2]
    if 1750<=i<=1950 and (vv>200).sum()>500: m[1005:1178,275:455]=1   # mao 'clique' inteira (contorno preto)
    if m.sum()==0: continue
    if os.path.exists(f'_tmp/lama/{i:04d}.png'): continue
    cv2.imwrite(f'_tmp/mask/{i:04d}.png',m*255)
    out=f.copy()
    for (r0,r1) in ((440,840),(760,1180)):
        mm=m[r0:r1]
        if mm.sum()==0: continue
        for tent in range(6):
            try:
                r=lama(Image.fromarray(cv2.cvtColor(f[r0:r1],cv2.COLOR_BGR2RGB)),Image.fromarray(mm*255)); break
            except RuntimeError as ex:
                print('retry',i,ex,flush=True); torch.cuda.empty_cache(); time.sleep(5)
        out[r0:r1]=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:r1-r0,:720]
    cv2.imwrite(f'_tmp/lama/{i:04d}.png',out[440:1180])
    if (i-a0+1)%200==0: el=time.time()-t0; print(f"[{i-a0+1}/{a1-a0}] {100*(i-a0+1)//(a1-a0)}% falta ~{el/(i-a0+1)*(a1-i-1)/60:.1f} min",flush=True)
print("ok",time.time()-t0)


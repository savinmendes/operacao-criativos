"""Troca o trecho s08 do AD 01 (01: quadros 1470-1807 = 02: 1514-1851) na base_lipsync.mp4 do 02 pela saida speed recortada
(lipsync/ad01_s08_speed.mp4, mesma entrada crop_s08_pt.mp4 do AD 01), colada com o colar.py do AD 01 na base_sem_legenda do AD 01.
Inicio (q1514) = corte real; fim (q1851|1852) = mesma tomada -> crossfade de 2 quadros. Reescreve base_lipsync.mp4 (antiga -> _tmp/base_lipsync_s08antigo.mp4)."""
import sys, shutil, subprocess, cv2, numpy as np
from pathlib import Path
AD=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(AD.parent/"ad01/lipsync2")); import colar as C
A0,A1,OFF=1470,1807,44
old=AD/"_tmp/base_lipsync_s08antigo.mp4"
if not old.exists(): shutil.move(str(AD/"base_lipsync.mp4"),str(old))
g=C.reamostrar(C.ler(AD/"lipsync/ad01_s08_speed.mp4"),A1-A0+1)
b01=cv2.VideoCapture(str(AD.parent/"ad01/base_sem_legenda.mp4")); b01.set(cv2.CAP_PROP_POS_FRAMES,A0)
novo=[]
for k in range(A1-A0+1):
    ok,bf=b01.read(); novo.append(C.colar(bf,g[k]))
src=cv2.VideoCapture(str(old))
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-threads","4",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD/"base_lipsync.mp4")],stdin=subprocess.PIPE)
i=0; q0,q1=A0+OFF,A1+OFF
while True:
    ok,f=src.read()
    if not ok: break
    if q0<=i<=q1: f=novo[i-q0]
    if i==q1+1:   # crossfade 2q na emenda continua
        L=novo[-1].astype(np.float32); R=f.astype(np.float32)
        f=np.clip(L/3+R*2/3,0,255).astype(np.uint8)
    if i==q1:
        ok2=True
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i+=1
ff.stdin.close(); ff.wait(); print("ok quadros",i)

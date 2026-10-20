"""base_sem_legenda.mp4 do 02 (30 fps, bt709/tv, sem audio): quadros 0-285 = gancho com LaMa (colado so na mascara, EMA leve);
quadros 286+ = base_sem_legenda.mp4 do AD 01 a partir do quadro 242 (mesmas imagens, deslocamento de 44 quadros, legenda ja removida com LaMa)."""
import subprocess, cv2, numpy as np
R0,R1=820,970; N=286; OFF=44
MK=np.load('_tmp/lama_mask.npy')
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda.mp4"],stdin=subprocess.PIPE)
cap=cv2.VideoCapture('../../../UNICOS_HD/02.mp4'); ema=None
for i in range(N):
    ok,f=cap.read(); m=MK[i].astype(np.float32)
    if m.sum()>0:
        l=cv2.imread(f'_tmp/lama/{i:04d}.png').astype(np.float32)
        ema=l if ema is None else 0.65*l+0.35*ema
        a=np.maximum(cv2.GaussianBlur(m,(11,11),0),m)[...,None]
        roi=f[R0:R1].astype(np.float32); f[R0:R1]=np.clip(ema*a+roi*(1-a),0,255).astype(np.uint8)
    else: ema=None
    ff.stdin.write(f.tobytes())
b=cv2.VideoCapture('../ad01/base_sem_legenda.mp4'); b.set(cv2.CAP_PROP_POS_FRAMES, N-OFF); k=N
while True:
    ok,f=b.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); k+=1
ff.stdin.close(); ff.wait(); print("ok quadros", k)

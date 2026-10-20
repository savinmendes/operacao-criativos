"""base_sem_legenda.mp4 do AD 06 (24 fps, quadros 0-2464 = 0-102,7 s; a tela final da cruz fica de fora), sem áudio, bt709 tv.
Faixa y 740-1090: LaMa (GPU) colado só na máscara (legenda PT + setas/brilhos do original), borda suave, EMA leve zerada nos cortes."""
import subprocess, cv2, numpy as np
R0,R1=740,1090; N=2465
CORTES=set(range(200,214))|{209,442,677,909,958,1298,1474,1714,1831,1905,1987,2072,2190,2319,2381,2413}
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
cap=cv2.VideoCapture('../../../UNICOS_HD/06.mp4')
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an","-threads","4",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda.mp4"],stdin=subprocess.PIPE)
ema=None
for i in range(N):
    ok,f=cap.read()
    if i in CORTES: ema=None
    m=np.load(f'_tmp/mask/{i:04d}.npy').astype(np.float32)
    if m.sum()>0:
        l=cv2.imread(f'_tmp/lama/{i:04d}.png').astype(np.float32)
        ema=l if ema is None else 0.65*l+0.35*ema
        al=np.maximum(cv2.GaussianBlur(m,(11,11),0),m)[...,None]
        roi=f[R0:R1].astype(np.float32); f[R0:R1]=np.clip(ema*al+roi*(1-al),0,255).astype(np.uint8)
    else: ema=None
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok")

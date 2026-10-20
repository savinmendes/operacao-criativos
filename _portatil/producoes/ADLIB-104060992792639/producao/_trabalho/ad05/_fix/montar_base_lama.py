"""base_sem_legenda_lama.mp4 (24 fps, tempo NOVO = original sem os quadros 1286-1355, 2298 quadros, sem áudio).
Faixa da legenda: LaMa GPU (_fix/lama/NNNN.png) colado só na máscara (borda suave), EMA leve dentro da máscara, zerada nos cortes."""
import subprocess, cv2, numpy as np
R0,R1=940,1110; N=2368; CA,CB=1286,1356
MK=np.load('_fix/lama_mask.npy',mmap_mode='r')
cap=cv2.VideoCapture('../../../UNICOS_HD/05.mp4')
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda_lama.mp4"],stdin=subprocess.PIPE)
ema=None; prev=None; cortes=[]
for i in range(N):
    ok,f=cap.read(); g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>20: ema=None; cortes.append(i)
    prev=g
    m=np.array(MK[i]).astype(np.float32)
    if m.sum()>0:
        l=cv2.imread(f'_fix/lama/{i:04d}.png').astype(np.float32)
        ema=l if ema is None else 0.65*l+0.35*ema
        a=np.maximum(cv2.GaussianBlur(m,(11,11),0),m)[...,None]
        roi=f[R0:R1].astype(np.float32); f[R0:R1]=np.clip(ema*a+roi*(1-a),0,255).astype(np.uint8)
    else: ema=None
    if CA<=i<CB: continue
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok cortes(orig):",cortes)

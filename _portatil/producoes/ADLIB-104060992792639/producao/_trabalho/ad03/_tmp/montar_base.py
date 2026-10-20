"""base_sem_legenda.mp4 do 03 (30 fps, bt709/tv, sem audio, todos os quadros):
- legenda PT e mao 'clique': LaMa (_tmp/lama, faixa y 440-1180) colado so na mascara com borda suave, EMA leve que zera nos cortes;
- split 1198-1436 (depoimento com PIX): metade de baixo (y 640-1280) trocada pela cruz dourada do proprio acervo (06.mp4, 108 s), _tmp/broll_cruz.mp4."""
import subprocess, cv2, numpy as np, os
R0,R1=440,1180; SPLIT=(1198,1436)
cap=cv2.VideoCapture('../../../UNICOS_HD/03.mp4'); cz=cv2.VideoCapture('_tmp/broll_cruz.mp4')
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an","-threads","4",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda.mp4"],stdin=subprocess.PIPE)
ema=None; prev=None; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.resize(f,(90,160)).astype(np.float32)
    if prev is not None and np.abs(g-prev).mean()>8: ema=None
    prev=g
    mp=f'_tmp/mask/{i:04d}.png'
    if os.path.exists(mp) and os.path.exists(f'_tmp/lama/{i:04d}.png'):
        m=(cv2.imread(mp,0)[R0:R1]>0).astype(np.float32)
        l=cv2.imread(f'_tmp/lama/{i:04d}.png').astype(np.float32)
        ema=l if ema is None else 0.65*l+0.35*ema
        a=np.maximum(cv2.GaussianBlur(m,(11,11),0),m)[...,None]
        roi=f[R0:R1].astype(np.float32); f[R0:R1]=np.clip(ema*a+roi*(1-a),0,255).astype(np.uint8)
    else: ema=None
    if SPLIT[0]<=i<=SPLIT[1]:
        ok2,c=cz.read(); assert ok2; f[640:1280]=c
    ff.stdin.write(f.tobytes()); i+=1
ff.stdin.close(); ff.wait(); print("ok quadros",i)

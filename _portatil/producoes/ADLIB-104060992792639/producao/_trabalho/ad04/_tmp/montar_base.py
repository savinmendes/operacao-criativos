"""base_sem_legenda.mp4 do AD 04 (30 fps, 2493 quadros, sem áudio, bt709 tv).
1) Faixa y 840-1210: LaMa (GPU) colado só na máscara (legenda PT + setas do original), borda suave, EMA leve zerada nos cortes.
2) Troca das cenas com depoimento financeiro (guincho 1586-1719 e aperto de mão/carro 1906-2003): a metade de baixo
   (y >= 580, rampa 520-580) vira o overlay dos anjos em oração do próprio vídeo (quadros 1046-1179 e 1186-1283, já limpos)."""
import subprocess, cv2, numpy as np
R0,R1=840,1210; N=2493
CORTES=set(range(284,308))|{290,293,523,602,669,810,1043,1292,1586,1720,1906,2004}
TROCA=[(1586,1720,1046),(1906,2004,1186)]
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
alpha=np.zeros((1280,1,1),np.float32); alpha[580:]=1; alpha[520:580,0,0]=np.linspace(0,1,60)
cap=cv2.VideoCapture('../../../UNICOS_HD/04.mp4')
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda.mp4"],stdin=subprocess.PIPE)
cache={}; precisa=set()
for a,b,s in TROCA: precisa|=set(range(s,s+(b-a)))
ema=None; buf=[]
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
    if i in precisa: cache[i]=f.copy()
    for a,b,s in TROCA:
        if a<=i<b:
            g=cache[s+i-a].astype(np.float32)
            f=np.clip(g*alpha+f.astype(np.float32)*(1-alpha),0,255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
    if (i+1)%500==0: print(f"[{i+1}/{N}]",flush=True)
ff.stdin.close(); ff.wait(); print("ok")

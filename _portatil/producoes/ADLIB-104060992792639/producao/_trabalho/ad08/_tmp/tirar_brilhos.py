"""2ª passada: tira os 'brilhos' brancos (triângulos) que acompanham a seta vermelha (já removida), com LaMa GPU.
Máscara = branco puro (V>235, S<30) na caixa x 200-520, y 650-1050, dilatada 9. base_sem_legenda.mp4 -> base_sem_legenda_v2.mp4"""
import subprocess, cv2, numpy as np, warnings; warnings.filterwarnings("ignore")
from PIL import Image
from simple_lama_inpainting import SimpleLama
X0,X1,Y0,Y1=200,520,650,1050
lama=SimpleLama(); cap=cv2.VideoCapture('base_sem_legenda.mp4')
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an","-threads","4",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda_v2.mp4"],stdin=subprocess.PIPE)
i=0; n=0
while True:
    ok,f=cap.read()
    if not ok: break
    if i>=2250:
        r=f[Y0:Y1,X0:X1]; hsv=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
        w=((hsv[...,2]>235)&(hsv[...,1]<30)).astype(np.uint8)
        if w.sum()>30:
            m=cv2.dilate(w,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
            C0,C1,D0,D1=100,620,550,1150; crop=f[D0:D1,C0:C1].copy(); mk=np.zeros(crop.shape[:2],np.uint8)
            mk[Y0-D0:Y1-D0,X0-C0:X1-C0]=m
            out=lama(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),Image.fromarray(mk*255))
            out=cv2.cvtColor(np.array(out),cv2.COLOR_RGB2BGR)[:crop.shape[0],:crop.shape[1]]
            a=cv2.GaussianBlur(mk.astype(np.float32),(7,7),0); a=np.maximum(a,mk)[...,None]
            f[D0:D1,C0:C1]=np.clip(out*a+crop*(1-a),0,255).astype(np.uint8); n+=1
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i+=1
ff.stdin.close(); ff.wait(); print("ok",i,"quadros, tratados",n)

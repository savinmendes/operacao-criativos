"""Cola a saida do HeyGen do gancho (ls_h1_speed.mp4, recorte 360x640 em (290,200) escalado 2x) de volta na base limpa,
com borda suave de 24 px no recorte inteiro. Gera _tmp/gancho_ls.mp4 (286 quadros) e mede a diferenca fora do rosto."""
import cv2, numpy as np, subprocess
X,Y,W,H=290,200,360,640
m=np.zeros((H,W),np.float32); m[24:-24,24:-24]=1; m=cv2.GaussianBlur(m,(0,0),10)[...,None]
b=cv2.VideoCapture('base_sem_legenda.mp4'); g=cv2.VideoCapture('lipsync/ls_h1_speed.mp4')
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-c:v","libx264","-crf","12","-pix_fmt","yuv420p",*COR,"_tmp/gancho_ls.mp4"],stdin=subprocess.PIPE)
d=[]
for i in range(286):
    ok,f=b.read(); ok2,o=g.read(); assert ok and ok2
    c=cv2.resize(o,(W,H),interpolation=cv2.INTER_AREA).astype(np.float32); roi=f[Y:Y+H,X:X+W].astype(np.float32)
    d.append(float(np.abs(c[400:600]-roi[400:600]).mean()))
    f[Y:Y+H,X:X+W]=np.clip(c*m+roi*(1-m),0,255).astype(np.uint8); ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("dif media fora do rosto (faixa inferior do recorte):",round(np.mean(d),2),"max",round(max(d),2))

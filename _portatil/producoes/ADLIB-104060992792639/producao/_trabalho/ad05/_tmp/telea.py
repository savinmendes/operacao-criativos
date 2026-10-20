"""Remove legenda amarela (faixa y 960-1090) por quadro com máscara justa (glifo + contorno) e inpaint OpenCV.
Uso: python telea.py [teste]  -> _tmp/semleg_orig.mp4 (24 fps, tempo original, quadros 0..2367, sem áudio)"""
import sys, subprocess, cv2, numpy as np
SRC='../../../UNICOS_HD/05.mp4'; OUT='_tmp/semleg_orig.mp4'; Y0,Y1=960,1090; N=2368
def mask(roi):
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    yel=((h>=15)&(h<=42)&(s>=80)&(v>=140)).astype(np.uint8)
    dark=cv2.dilate((v<90).astype(np.uint8),np.ones((7,7),np.uint8))
    core=yel&dark
    # só componentes perto de texto: fecha e filtra por linha
    core=cv2.morphologyEx(core,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    m=cv2.dilate(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
    # contorno preto da legenda: pixels escuros colados ao glifo
    out=(v<110).astype(np.uint8)&cv2.dilate(core,np.ones((9,9),np.uint8))
    return cv2.dilate(m|out,np.ones((5,5),np.uint8))
def proc(f):
    roi=f[Y0-20:Y1+20].copy(); m=mask(roi)
    if m.sum()<30: return f
    r=cv2.inpaint(roi,m,5,cv2.INPAINT_TELEA)
    a=cv2.GaussianBlur(m.astype(np.float32),(5,5),0)[...,None]; a=np.maximum(a,m[...,None].astype(np.float32))
    g=f.copy(); g[Y0-20:Y1+20]=np.clip(r*a+roi*(1-a),0,255).astype(np.uint8); return g
c=cv2.VideoCapture(SRC)
if len(sys.argv)>1:
    rows=[]
    for i in [30,100,150,230,400,800,960,1300,1600,2000]:
        c.set(1,i); ok,f=c.read(); g=proc(f); rows.append(np.hstack([f[900:1150],g[900:1150]]))
    cv2.imwrite('_tmp/telea_teste.jpg',np.vstack(rows)); sys.exit()
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",OUT],stdin=subprocess.PIPE)
for i in range(N):
    ok,f=c.read(); ff.stdin.write(np.ascontiguousarray(proc(f)).tobytes())
    if i%240==0: print(f"[{i}/{N}] {100*i//N}%",flush=True)
ff.stdin.close(); ff.wait(); print("ok",OUT)

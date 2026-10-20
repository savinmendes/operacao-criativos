# Compõe o AD IT: base sem legenda ES (LaMa) + boca/queixo do lipsync HeyGen (elipse suave por quadro, landmarks)
# + legenda IT (ASS) + mix (voz IT + trilha demucs). Saída 1080x1920 30 fps.
import cv2, numpy as np, subprocess, json, mediapipe as mp
from pathlib import Path
from comum3 import quadros, ENC_TAG
MOD=str(Path.home()/".cache"/"kit-edicao"/"face_landmarker.task")
det=mp.tasks.vision.FaceLandmarker.create_from_options(mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=MOD),num_faces=1))
SEG=json.load(open("heygen_in/seg.json"))
base=list(quadros("base_limpa.mp4")); N=len(base); print("base",N)
src=list(quadros("fontes/es.mp4"))
def lm(img):
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))))
    if not r.face_landmarks: return None
    p=np.array([(q.x*img.shape[1],q.y*img.shape[0]) for q in r.face_landmarks[0]]); return p
out=[f.copy() for f in base]
# carimbo OVERDUTE -> SCADUTO (plano estático do gancho, quadros 0-151)
PT=np.load("scaduto_patch.npy").astype(np.float32); MK=np.load("scaduto_mask.npy")[...,None]
for k in range(152):
    r=out[k][360:480,460:720].astype(np.float32); out[k][360:480,460:720]=np.clip(PT*MK+r*(1-MK),0,255).astype(np.uint8)
base=[f.copy() for f in out]
for nm,(q0,q1,cx) in SEG.items():
    hg=list(quadros(f"heygen/{nm}_out.mp4")); n=min(len(hg),q1-q0)
    P=[]
    for k in range(n):
        g=hg[k]; p=lm(g)
        if cx:  # recorte -> de volta ao quadro (landmarks no recorte, só o Jesus)
            x,y,w,h=cx; full=src[q0+k].copy(); full[y:y+h,x:x+w]=cv2.resize(g,(w,h),interpolation=cv2.INTER_AREA); g=full
            if p is not None: p=p*np.array([w/720,h/1280])+np.array([x,y])
        hg[k]=g
        P.append(None if p is None else np.array([p[[61,291]].mean(0)[0],p[[13,14,17,152]].mean(0)[1],np.linalg.norm(p[234]-p[454])]))
    ok=[x for x in P if x is not None]; med=np.median(ok,0); print(nm,"rosto em",len(ok),"/",n,"centro/larg",med.round(1))
    P=[med if x is None else x for x in P]
    P=np.array(P); Ps=np.array([P[max(0,k-2):k+3].mean(0) for k in range(n)])
    # desvio de cor: fora da boca, saída HeyGen x fonte (anel do rosto)
    dv=[]
    for k in range(0,n,10):
        cxm,cym,fw=Ps[k]; r=(slice(int(cym-0.55*fw),int(cym-0.25*fw)),slice(int(cxm-0.3*fw),int(cxm+0.3*fw)))
        dv.append((src[q0+k][r].astype(np.float32)-hg[k][r].astype(np.float32)).mean((0,1)))
    dv=np.mean(dv,0); print(nm,"desvio cor",dv.round(2))
    for k in range(n):
        cxm,cym,fw=Ps[k]; m=np.zeros((1280,720),np.float32)
        cv2.ellipse(m,(int(cxm),int(cym)),(int(0.36*fw),int(0.30*fw)),0,0,360,1.0,-1)
        m=cv2.GaussianBlur(m,(0,0),max(3,0.06*fw))[...,None]
        g=np.clip(hg[k].astype(np.float32)+dv,0,255)
        out[q0+k]=np.clip(g*m+base[q0+k]*(1-m),0,255).astype(np.uint8)
TOTAL=31.6; NT=int(round(TOTAL*30))
vf=("[0:v]scale=1080:1920:flags=lanczos,ass=leg_it.ass:fontsdir=fonts,"
    "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-i","audio/mix_it.wav","-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","17","-preset","medium",
    "-maxrate","9M","-bufsize","18M",*ENC_TAG,"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}","-movflags","+faststart",
    "bruto_it.mp4"],stdin=subprocess.PIPE)
for k in range(NT): enc.stdin.write(out[min(k,N-1)].tobytes())
enc.stdin.close(); enc.wait(); print("ok bruto_it.mp4")

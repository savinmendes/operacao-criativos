# AD FR: base_fr (sem texto ES, cenas na linha do tempo FR) + boca/queixo do lipsync HeyGen (elipse suave por landmarks,
# cor corrigida pelo anel do rosto) + título FR (PNG) + legenda/CTA FR (ASS) + mix. Saída 1080x1920 30 fps, bt601 fixo.
import cv2, numpy as np, subprocess, json, sys, mediapipe as mp
from pathlib import Path
from comum3 import quadros, ENC_TAG
W,H=1080,1920; FPS=30
MOD=str(Path.home()/".cache"/"kit-edicao"/"face_landmarker.task")
det=mp.tasks.vision.FaceLandmarker.create_from_options(mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=MOD),num_faces=1))
T=json.load(open("timeline.json",encoding="utf-8")); NT=int(round(T["total"]*FPS))
SEG=json.load(open("heygen_in/seg.json")); SAIDA=sys.argv[1] if len(sys.argv)>1 else "bruto_fr.mp4"
SEM_LS=len(sys.argv)>2 and sys.argv[2]=="--sem-lipsync"
def lm(img):
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))))
    if not r.face_landmarks: return None
    return np.array([(q.x*img.shape[1],q.y*img.shape[0]) for q in r.face_landmarks[0]])
seg_q={nm:(int(round(a*FPS)),int(round(b*FPS))) for nm,(a,b) in SEG.items()}
def prepara(nm,base_frames):
    q0,q1=seg_q[nm]; hg=[]
    for g in quadros(f"heygen/{nm}_out.mp4",w=W,h=H): hg.append(g)
    n=min(len(hg),q1-q0); P=[]
    for k in range(n):
        p=lm(hg[k]); P.append(None if p is None else np.array([p[[61,291]].mean(0)[0],p[[13,14,17,152]].mean(0)[1],np.linalg.norm(p[234]-p[454])]))
    ok=[x for x in P if x is not None]; med=np.median(ok,0); print(nm,"rosto",len(ok),"/",n,"hg",len(hg),"seg",q1-q0,med.round(1),flush=True)
    P=np.array([med if x is None else x for x in P]); Ps=np.array([P[max(0,k-2):k+3].mean(0) for k in range(n)])
    dv=[]
    for k in range(0,n,6):
        cx,cy,fw=Ps[k]; r=(slice(int(cy-0.55*fw),int(cy-0.25*fw)),slice(int(cx-0.3*fw),int(cx+0.3*fw)))
        dv.append((base_frames[k][r].astype(np.float32)-hg[k][r].astype(np.float32)).mean((0,1)))
    dv=np.mean(dv,0); print(nm,"desvio cor",dv.round(2),flush=True)
    out=[]
    for k in range(q1-q0):
        b=base_frames[k]
        if k>=n: out.append(b); continue
        cx,cy,fw=Ps[k]; m=np.zeros((H,W),np.float32)
        cv2.ellipse(m,(int(cx),int(cy)),(int(0.36*fw),int(0.30*fw)),0,0,360,1.0,-1)
        m=cv2.GaussianBlur(m,(0,0),max(3,0.06*fw))[...,None]
        g=np.clip(hg[k].astype(np.float32)+dv,0,255)
        out.append(np.clip(g*m+b*(1-m),0,255).astype(np.uint8))
    return out
vf=("[0:v]ass=leg_fr.ass:fontsdir=fonts[a];[a][2:v]overlay=0:0:enable='lt(t,4.9)'[b];"
    "[b]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-",
    "-i","audio/mix_fr.wav","-loop","1","-i","titulo_fr.png","-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","18","-preset","medium",
    "-maxrate","10M","-bufsize","20M",*ENC_TAG,"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{T['total']:.3f}","-movflags","+faststart",
    SAIDA],stdin=subprocess.PIPE)
buf=[]; k=0
for f in quadros("base_fr.mp4",w=W,h=H):
    if k>=NT: break
    nm=None if SEM_LS else next((n for n,(a,b) in seg_q.items() if a<=k<b),None)
    if nm:
        buf.append(f)
        if k==seg_q[nm][1]-1:
            for o in prepara(nm,buf): enc.stdin.write(o.tobytes())
            buf=[]
    else:
        enc.stdin.write(f.tobytes())
    k+=1
# completa com o último quadro se a base for curta
while k<NT: enc.stdin.write(f.tobytes()); k+=1
enc.stdin.close(); enc.wait(); print("ok",SAIDA,k)

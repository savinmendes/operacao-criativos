# AD EN: base_en (sem texto ES, cenas na linha do tempo EN)
#  + comerciante: boca/queixo do lipsync HeyGen speed (elipse suave por landmarks, cor corrigida pelo anel do rosto), sem retoque
#  + padre: HeyGen Avatar IV gerado do zero (720p 25 fps -> lanczos 1080x1920, quadro mais próximo em 30 fps, cor casada em Lab
#    com a imagem base), setas amarelas do CTA copiadas da base
#  + título EN (PNG) + legenda/CTA EN (ASS) + mix. Saída 1080x1920 30 fps, bt601 fixo.
import cv2, numpy as np, subprocess, json, sys, mediapipe as mp
from pathlib import Path
from comum3 import quadros, ENC_TAG
W,H=1080,1920; FPS=30
MOD=str(Path.home()/".cache"/"kit-edicao"/"face_landmarker.task")
det=mp.tasks.vision.FaceLandmarker.create_from_options(mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=MOD),num_faces=1))
T=json.load(open("timeline.json",encoding="utf-8")); NT=int(round(T["total"]*FPS))
SAIDA=sys.argv[1] if len(sys.argv)>1 else "SB-EN-AVATAR-REST_v1.mp4"
q=lambda t:int(round(t*FPS))
SEGC={c["nome"]:(q(c["out_ini"]),q(c["out_fim"])) for c in T["cenas"] if c["lipsync"]=="comerciante"}
OFF=json.load(open("padre/padre_hg_offsets.json"))
SEGP={nm:(q(a),q(b),o,a) for nm,(o,a,b) in OFF.items()}
def lm(img):
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))))
    if not r.face_landmarks: return None
    return np.array([(p.x*img.shape[1],p.y*img.shape[0]) for p in r.face_landmarks[0]])
def prepara(nm,base_frames):
    q0,q1=SEGC[nm]
    if not Path(f"heygen/{nm}_out.mp4").exists(): print(nm,"SEM LIPSYNC (prévia)"); return base_frames
    hg=list(quadros(f"heygen/{nm}_out.mp4",w=W,h=H))
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
# padre
hgp=list(quadros("padre/padre_hg_720.mp4",w=720,h=1280)); print("hg padre",len(hgp))
ref=cv2.imread("cand/k1202_limpo.png")
def lab_stats(img): l=cv2.cvtColor(img,cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32); return l.mean(0),l.std(0)
up=lambda g: cv2.resize(g,(W,H),interpolation=cv2.INTER_LANCZOS4)
mr,sr=lab_stats(ref); S=[lab_stats(up(hgp[i])) for i in range(0,len(hgp),25)]
mh=np.mean([s[0] for s in S],0); sh=np.mean([s[1] for s in S],0); print("Lab ref",mr.round(1),sr.round(1),"hg",mh.round(1),sh.round(1))
def cor(g):
    l=cv2.cvtColor(g,cv2.COLOR_BGR2LAB).astype(np.float32); l=(l-mh)/sh*sr+mr
    return cv2.cvtColor(np.clip(l,0,255).astype(np.uint8),cv2.COLOR_LAB2BGR)
def setas(v1,novo):
    y0=1560; r=v1[y0:]; hsv=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
    am=((hsv[...,0]>=18)&(hsv[...,0]<=40)&(hsv[...,1]>=90)&(hsv[...,2]>=150)).astype(np.uint8)
    n,lab,st,_=cv2.connectedComponentsWithStats(am)
    keep=np.zeros_like(am)
    for k in range(1,n):
        if st[k,cv2.CC_STAT_AREA]>4000:
            mk=lab==k; h,v=hsv[mk].mean(0)[0],hsv[mk].mean(0)[2]
            if h>=24 and v>=225:
                x,y,w,hh=st[k,:4]; y1=max(0,y-90)
                sub=hsv[y1:y+hh,max(0,x-4):x+w+4]
                pale=((sub[...,0]>=15)&(sub[...,0]<=45)&(sub[...,1]>=35)&(sub[...,2]>=205)).astype(np.uint8)
                n2,l2,s2,_=cv2.connectedComponentsWithStats(pale|mk[y1:y+hh,max(0,x-4):x+w+4].astype(np.uint8))
                big=1+np.argmax(s2[1:,4]); keep[y1:y+hh,max(0,x-4):x+w+4]|=(l2==big).astype(np.uint8)
    if keep.sum()==0: return novo
    keep=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    d=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    m=(keep|(d&(hsv[...,2]<80).astype(np.uint8))).astype(np.float32)
    m=cv2.GaussianBlur(m,(3,3),0)[...,None]
    out=novo.copy(); out[y0:]=(r*m+novo[y0:]*(1-m)).astype(np.uint8); return out
LOG=[]
def padre(k,base):
    for nm,(q0,q1,o,a) in SEGP.items():
        if q0<=k<q1:
            th=o+k/FPS-a; i=min(len(hgp)-1,int(round(th*25))); LOG.append((k,nm,i))
            return setas(base,cor(up(hgp[i])))
    return None
vf=("[0:v]ass=leg_en.ass:fontsdir=fonts[a];[a][2:v]overlay=0:0:enable='lt(t,4.9)'[b];"
    "[b]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-",
    "-i","audio/mix_en.wav","-loop","1","-i","titulo_en.png","-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","18","-preset","medium",
    "-maxrate","10M","-bufsize","20M",*ENC_TAG,"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{T['total']:.3f}","-movflags","+faststart",
    SAIDA],stdin=subprocess.PIPE)
buf=[]; k=0
for f in quadros("base_en.mp4",w=W,h=H):
    if k>=NT: break
    nm=next((n for n,(a,b) in SEGC.items() if a<=k<b),None)
    if nm:
        buf.append(f)
        if k==SEGC[nm][1]-1:
            for o in prepara(nm,buf): enc.stdin.write(o.tobytes())
            buf=[]
    else:
        p=padre(k,f); enc.stdin.write((f if p is None else p).tobytes())
    k+=1
while k<NT: enc.stdin.write(f.tobytes()); k+=1
enc.stdin.close(); enc.wait(); json.dump(LOG,open("padre/mapa_padre.json","w")); print("ok",SAIDA,k,"padre",len(LOG))

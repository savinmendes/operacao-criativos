# v2: vídeo v1 (fora das cenas do padre) + padre novo do HeyGen Avatar IV (720p 25 fps -> lanczos 1080x1920, quadro mais próximo
# em 30 fps, cor casada com o take original por transferência média/desvio em Lab) nas 5 cenas do padre; setas do CTA copiadas
# do v1 (amarelo + contorno preto); legenda FR (ASS deslocado -1 s) por cima só nas cenas do padre; áudio mix_v3.wav (receita do chiado). bt601 fixa.
import sys, json, subprocess, cv2, numpy as np
sys.path.insert(0,'..'); from comum3 import quadros, ENC_TAG
W,H,FPS=1080,1920,30; TOT=61.3; NT=int(round(TOT*FPS))
OFF=json.load(open("padre_hg_offsets.json"))   # nome: [hg_ini, pre_ini, pre_fim]  (linha do tempo antes dos jump cuts)
# o padre entra 1 quadro antes da 1a palavra (sem boca aberta no silêncio do começo do plano): o b-roll anterior cobre o
# silêncio, com o último 1 s dele levemente alongado (repetição de quadro, fator <= 1,25)
WD=json.load(open("../palavras_fr.json",encoding="utf-8"))
SEGS=[]; ESTICA=[]
REAL={"S7_padre1":(840,952),"S10_padre2":(1111,1197),"S12_padre3":(1317,1383),"S15_padre4":(1512,1601),"S17_padre5":(1661,1733)}
for nm,(o,a,b) in OFF.items():
    q0,q1=REAL[nm]   # cortes reais do v1 (medidos), não o arredondamento da timeline
    first=min(x[1] for x in WD if a<=x[1]<b); qn=max(q0,int(np.floor((first-1.0)*FPS))-1)
    if qn-q0>=3: ESTICA.append((q0-30,q0-1,qn)); q0n=qn   # q0-1 fica fora: no v1 o quadro antes do corte pode ter remendo de boca
    else: q0n=q0
    SEGS.append((nm,q0n,q1,o,a)); print(nm,"entra",q0n-q0,"quadros depois")
def fonte_v1(k):
    for e0,e1,e2 in ESTICA:
        if e0<=k<e2: return e0+int((k-e0)*(e1-e0)/(e2-e0))
    return k
hg=list(quadros("padre_hg_720.mp4",w=720,h=1280)); print("hg",len(hg))
ref=cv2.imread("cand/k1202_limpo.png")
def lab_stats(img): l=cv2.cvtColor(img,cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32); return l.mean(0),l.std(0)
up=lambda g: cv2.resize(g,(W,H),interpolation=cv2.INTER_LANCZOS4)
mr,sr=lab_stats(ref); S=[lab_stats(up(hg[i])) for i in range(0,len(hg),25)]
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
            mk=lab==k; h,_,v=hsv[mk].mean(0)[0],0,hsv[mk].mean(0)[2]
            if h>=24 and v>=225:
                x,y,w,hh=st[k,:4]; y1=max(0,y-90)
                sub=hsv[y1:y+hh,x-4:x+w+4]
                pale=((sub[...,0]>=15)&(sub[...,0]<=45)&(sub[...,1]>=35)&(sub[...,2]>=205)).astype(np.uint8)
                n2,l2,s2,_=cv2.connectedComponentsWithStats(pale|mk[y1:y+hh,x-4:x+w+4].astype(np.uint8))
                big=1+np.argmax(s2[1:,4]); keep[y1:y+hh,x-4:x+w+4]|=(l2==big).astype(np.uint8)
    if keep.sum()==0: return novo
    keep=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    d=cv2.dilate(keep,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    m=(keep|(d&(hsv[...,2]<80).astype(np.uint8))).astype(np.float32)
    m=cv2.GaussianBlur(m,(3,3),0)[...,None]
    out=novo.copy(); out[y0:]=(r*m+novo[y0:]*(1-m)).astype(np.uint8); return out
import re
def _p(x): h,m,y=x.split(":"); return int(h)*3600+int(m)*60+float(y)
def _f(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
LA=[]
for l in open("leg_v2_cut.ass",encoding="utf-8").read().splitlines():
    mm=re.match(r"Dialogue: (\d+),([\d:.]+),([\d:.]+),(.*)",l)
    if mm:
        a0=_p(mm.group(2))
        for _,q0,_,_,_ in SEGS:
            if q0/FPS<a0<=q0/FPS+0.15: a0=q0/FPS   # sem piscada de legenda na entrada do padre
        l=f"Dialogue: {mm.group(1)},{_f(a0)},{mm.group(3)},{mm.group(4)}"
    LA.append(l)
open("leg_v3.ass","w",encoding="utf-8").write(chr(10).join(LA)+chr(10))
def leg(cor):
    p=subprocess.Popen(["ffmpeg","-v","error","-f","lavfi","-i",f"color=c={cor}:s={W}x{H}:r=30:d={TOT}","-vf","ass=leg_v3.ass:fontsdir=fonts",
        "-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3)
LB=leg("black"); LW=leg("white")
def com_legenda(f,pb,pw):
    a=1-(pw.astype(np.float32)-pb.astype(np.float32)).mean(2,keepdims=True)/255
    if a.max()<0.01: return f
    a=np.clip(cv2.GaussianBlur(a,(0,0),0.8)[...,None] if a.ndim==3 else a,0,1)
    a=a.reshape(H,W,1); c=pb.astype(np.float32)/np.maximum(a,1e-3)
    c=cv2.GaussianBlur(c,(0,0),0.6)
    return np.clip(c*a+f*(1-a),0,255).astype(np.uint8)
en=" + ".join(f"between(t,{a/FPS:.4f},{(b-0.5)/FPS:.4f})" for _,a,b,_,_ in SEGS)
vf=("[0:v]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
SAIDA=sys.argv[1] if len(sys.argv)>1 else "SB-FR-AVATAR-REST_v2.mp4"
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-i","mix_v3.wav",
    "-filter_complex",vf,"-map","[v]","-map","1:a","-c:v","libx264","-crf","18","-preset","medium","-maxrate","10M","-bufsize","20M",*ENC_TAG,
    "-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOT:.3f}","-movflags","+faststart",SAIDA],stdin=subprocess.PIPE)
log=[]; V1=list(quadros("../SB-FR-AVATAR-REST_v1.mp4",w=W,h=H)) if False else None
import collections
cache=collections.OrderedDict(); src=quadros("../SB-FR-AVATAR-REST_v1.mp4",w=W,h=H); lido=-1
def v1(j):
    global lido
    while lido<j:
        cache[lido+1]=next(src); lido+=1
        while len(cache)>40: cache.popitem(last=False)
    return cache[j]
for k in range(NT):
    f=v1(fonte_v1(k)); f=f.copy(); pb=next(LB); pw=next(LW)
    s=next((x for x in SEGS if x[1]<=k<x[2]),None)
    if s:
        nm,a,b,o,pa=s; th=o+k/FPS-(pa-1.0); i=min(len(hg)-1,int(round(th*25)))
        f=com_legenda(setas(f,cor(up(hg[i]))),pb,pw); log.append((k,nm,i))
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
json.dump(log,open("mapa_padre.json","w")); print("ok",SAIDA,k+1,"quadros; padre",len(log))

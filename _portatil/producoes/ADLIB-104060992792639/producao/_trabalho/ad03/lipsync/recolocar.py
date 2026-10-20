"""base_lipsync.mp4 do 03: cola cada saida do HeyGen (lipsync/ls_<nome>.mp4, recorte 360x640 em (170,0) escalado 2x) na base limpa,
no recorte inteiro com borda suave de 24 px (a borda de baixo do recorte, y 640, tem 24 px de transicao). Reamostra no tempo se vier
com quadros a menos (interpolacao, sem congelar). Emendas entre trechos da mesma tomada (sem corte na base): crossfade de 2 quadros."""
import json, subprocess, cv2, numpy as np
from pathlib import Path
L=Path(__file__).parent; AD=L.parent
J=json.loads((L/"trechos.json").read_text(encoding="utf-8-sig")); X,Y,W,H=J["recorte"]
M=np.zeros((H,W),np.float32); M[24:-24,24:-24]=1; M[:24,24:-24]=1   # topo do recorte = topo do quadro
M=cv2.GaussianBlur(M,(0,0),9)[...,None]; M[:4]=M[4]
def ler(p):
    cap=cv2.VideoCapture(str(p)); fr=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr,n):
    m=len(fr)
    if m==n: return fr
    out=[]
    for i in range(n):
        x=i*(m-1)/(n-1); j=int(np.floor(x)); a=x-j
        out.append(fr[j] if a<1e-3 or j>=m-1 else cv2.addWeighted(fr[j],1-a,fr[j+1],a,0))
    return out
base=cv2.VideoCapture(str(AD/"base_sem_legenda.mp4"))
COR=["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-threads","4",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD/"base_lipsync.mp4")],stdin=subprocess.PIPE)
i=0; prev=None; log=[]
def flush():
    global prev
    if prev:
        for f in prev[0]: ff.stdin.write(f.tobytes())
    prev=None
for nome,a,b in J["trechos"]:
    if i<a: flush()
    while i<a:
        ok,f=base.read(); ff.stdin.write(f.tobytes()); i+=1
    n=b-a+1; bases=[]
    for _ in range(n):
        ok,f=base.read(); bases.append(f); i+=1
    g=ler(L/f"ls_{nome}.mp4"); info=len(g)
    if len(g)>n+2: g=g[:n]          # trechos completados ate 3 s: usa so os quadros reais
    g=reamostrar(g,n); fr=[]
    for bf,o in zip(bases,g):
        c=cv2.resize(o,(W,H),interpolation=cv2.INTER_AREA).astype(np.float32); roi=bf[Y:Y+H,X:X+W].astype(np.float32)
        out=bf.copy(); out[Y:Y+H,X:X+W]=np.clip(c*M+roi*(1-M),0,255).astype(np.uint8); fr.append(out)
    if prev is not None:
        corte=np.abs(prev[1].astype(np.float32)-bases[0]).mean()>10
        if not corte and prev[2]==a-1:
            Lf,Rf=prev[0][-1].astype(np.float32),fr[0].astype(np.float32)
            prev[0][-1]=np.clip(Lf*2/3+Rf/3,0,255).astype(np.uint8); fr[0]=np.clip(Lf/3+Rf*2/3,0,255).astype(np.uint8)
        log.append(f"{nome} q{a}: {'corte' if corte else 'crossfade 2q'}")
        flush()
    prev=(fr,bases[-1],b); print(nome,info,"->",n,flush=True)
flush()
while True:
    ok,f=base.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); i+=1
ff.stdin.close(); ff.wait(); print("\n".join(log)); print("ok quadros",i)

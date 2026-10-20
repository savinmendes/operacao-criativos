# Cola só boca+queixo do HeyGen (out) sobre o take original (in), com elipse suave, cor pelo anel de pele e nitidez casada.
# uso: python colar_boca.py in.mp4 out.mp4 dest.mp4 [--fechar ini:fim ...]  (janelas em s onde a boca volta ao original)
import sys,subprocess,numpy as np,cv2
sys.path.insert(0,r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
ina,outa,dest=sys.argv[1:4]; fech=[tuple(map(float,x.split(':'))) for x in sys.argv[5:]] if len(sys.argv)>4 and sys.argv[4]=='--fechar' else []
def info(p):
    o=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height,r_frame_rate','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip().split(',')
    a,b=o[2].split('/'); return int(o[0]),int(o[1]),int(a)/int(b)
def ler(p):
    w,h,f=info(p)
    pr=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf','scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24','-fps_mode','passthrough','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(pr,np.uint8).reshape(-1,h,w,3),f
A,fps=ler(ina); B,_=ler(outa); n=min(len(A),len(B)); A=A[:n]; B=B[:n]; H,W=A.shape[1:3]
det=cl.Rastreador(); geo=[]
for k in range(n):
    p=det.pontos(B[k])
    if p is None: geo.append(None); continue
    fw=np.linalg.norm(p[234]-p[454]); mouth=p[[13,14,61,291,0,17]].mean(0); chin=p[152]; nose=p[2]
    cx=mouth[0]*0.85+chin[0]*0.15; cy=(nose[1]*0.35+chin[1]*0.65)
    ax=0.36*fw; ay=(chin[1]-nose[1])*0.62
    geo.append((cx,cy,ax,ay,fw))
# preencher falhas e suavizar no tempo
idx=[i for i,g in enumerate(geo) if g is not None]; G=np.array([geo[i] for i in idx])
G=np.array([np.interp(np.arange(n),idx,G[:,j]) for j in range(5)]).T
from scipy.ndimage import uniform_filter1d
G=uniform_filter1d(G,size=5,axis=0,mode='nearest')
def mask(g):
    cx,cy,ax,ay,fw=g; m=np.zeros((H,W),np.float32)
    cv2.ellipse(m,(int(cx),int(cy)),(int(ax),int(ay)),0,0,360,1.0,-1)
    return cv2.GaussianBlur(m,(0,0),max(3,0.06*fw))
# cor: diferença no anel de pele (fora da elipse), mediana em quadros amostrados
ds=[]; lapA=[]; lapB=[]
for k in range(0,n,max(1,n//15)):
    m=mask(G[k]); dentro=m>0.02; cx,cy,ax,ay,fw=G[k]
    big=np.zeros((H,W),np.uint8); cv2.ellipse(big,(int(cx),int(cy)),(int(ax*1.35),int(ay*1.3)),0,0,360,1,-1)
    anel=(big>0)&~dentro
    ds.append(np.median(A[k][anel].astype(np.float32)-B[k][anel].astype(np.float32),0))
    x0,y0,x1,y1=int(cx-ax*0.7),int(cy-ay*0.7),int(cx+ax*0.7),int(cy+ay*0.7)
    lapA.append(cv2.Laplacian(cv2.cvtColor(A[k][y0:y1,x0:x1],cv2.COLOR_BGR2GRAY),cv2.CV_64F).var())
    lapB.append(cv2.Laplacian(cv2.cvtColor(B[k][y0:y1,x0:x1],cv2.COLOR_BGR2GRAY),cv2.CV_64F).var())
d=np.median(ds,0).astype(np.float32); la,lb=np.median(lapA),np.median(lapB)
# nitidez: unsharp com força escolhida para igualar a variância do Laplaciano do original
def sharp(f,amt,sig=1.2):
    bl=cv2.GaussianBlur(f,(0,0),sig); return cv2.addWeighted(f,1+amt,bl,-amt,0)
amt=0.0; k0=n//2; cx,cy,ax,ay,fw=G[k0]; x0,y0,x1,y1=int(cx-ax*0.7),int(cy-ay*0.7),int(cx+ax*0.7),int(cy+ay*0.7)
for t in np.arange(0,4.01,0.1):
    s=sharp(B[k0].astype(np.float32),t)[y0:y1,x0:x1]
    if cv2.Laplacian(cv2.cvtColor(np.clip(s,0,255).astype(np.uint8),cv2.COLOR_BGR2GRAY),cv2.CV_64F).var()>=la*0.9: amt=t; break
    amt=t
print(f'cor anel {d.round(1)} | nitidez boca orig {la:.0f} heygen {lb:.0f} -> unsharp {amt:.1f}')
def peso_fechar(t):
    w=1.0
    for a,b in fech:
        r=2/fps
        if a-r<=t<=b+r: w=min(w, 0.0 if a<=t<=b else (a-t)/r if t<a else (t-b)/r)
    return max(0.0,min(1.0,w))
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-vf','scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p','-c:v','libx264','-crf','10','-preset','medium',dest],stdin=subprocess.PIPE)
for k in range(n):
    m=mask(G[k])*peso_fechar(k/fps); m=m[...,None]
    b=sharp(B[k].astype(np.float32)+d,amt)
    o=b*m+A[k].astype(np.float32)*(1-m)
    enc.stdin.write(np.clip(o+0.5,0,255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok',dest,n,'quadros')

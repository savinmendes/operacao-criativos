# Compoe o AD IT (copiado do EN e adaptado): base limpa (LaMa) + trechos HeyGen (lipsync) + legenda EN no estilo do ES (caixa alta, brilho, palavra-chave colorida)
# + seta vermelha no CTA + audio mix. Cor bt601/tv fixa na leitura e gravacao.
import json, subprocess, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=720,1280,30; TOTAL=32.6; N=int(round(TOTAL*FPS))
CUTS=[0,5.467,10.4,15.0,19.067,23.367,26.5,TOTAL]   # cena 1 +0,4 s e cena 7 5,4->6,1 s (HeyGen alongado)
SHIFT=0.4  # base_limpa (linha do tempo ES) = t-0,4 depois da cena 1
YC=json.load(open("y_cena.json"))          # centro y da legenda por cena (medido no ES)
HG=json.load(open("heygen_trechos.json"))  # [[arquivo, t_ini, t_fim], ...]
FP=r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"
FONTS={0:ImageFont.truetype(FP,30)}; FBIG=ImageFont.truetype(FP,50)
XC={0:548}; WRAP={0:300}   # gancho: legenda menor, à direita (sob o Jesus pequeno), como no ES
CENA=lambda t:max(k for k in range(7) if CUTS[k]<=t+1e-6)
COR={"r":(255,32,32),"y":(255,240,40),"g":(60,255,60)}
OUT=sys.argv[1] if len(sys.argv)>1 else "bruto_it.mp4"
def decode(p,ss=0,dur=None):
    cmd=["ffmpeg","-v","error","-ss",f"{ss:.3f}","-i",p]+(["-t",f"{dur:.3f}"] if dur else [])+["-vf",
        f"fps={FPS},scale={W}:{H}:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24","-f","rawvideo","-"]
    raw=subprocess.run(cmd,capture_output=True).stdout; n=len(raw)//(W*H*3)
    return np.frombuffer(raw[:n*W*H*3],np.uint8).reshape(n,H,W,3)
base=decode("base_limpa.mp4"); print("base",len(base))
hg=[(decode(p),a,b) for p,a,b in HG]
if False:   # quadro 151 do HeyGen s1 saiu com a boca 'fantasma' (revisor): repete o 150
    f0=hg[0][0].copy(); f0[151]=f0[150]; hg[0]=(f0,hg[0][1],hg[0][2])
# ---- legenda
pal=json.load(open("audio/palavras_it.json",encoding="utf-8"))
bl=json.load(open("legenda_blocos.json",encoding="utf-8"))
blocos=[]; j=0
for fid,txt,cores in bl:
    n=len(txt.split()); ws=pal[j:j+n]; j+=n
    assert all(w[3]==fid for w in ws),(txt,ws)
    cm={k:v for k,v in (c.split(":") for c in cores.split(",") if c)}
    blocos.append([ws[0][1],ws[-1][2],txt,cm])
for i,b in enumerate(blocos):
    nx=blocos[i+1][0] if i+1<len(blocos) else TOTAL
    fim=nx-0.04 if nx-b[1]<1.2 else b[1]+0.5
    cut=min([c for c in CUTS if c>b[0]+0.05]+[TOTAL])
    if b[1]<=cut: fim=min(fim,cut-0.01)   # legenda nao atravessa o corte de cena
    b.append(fim)
def render(txt,cm,sc_):
    FONT=FONTS.get(sc_,FBIG); LH=int(FONT.size*1.18); MAXW=WRAP.get(sc_,520)
    words=txt.split(); lines=[]; cur=[]
    for w in words:
        t=" ".join(cur+[w])
        if FONT.getlength(t)>MAXW and cur: lines.append(cur); cur=[w]
        else: cur.append(w)
    lines.append(cur)
    h=LH*len(lines)+40; img=Image.new("RGBA",(W,h),(0,0,0,0))
    txtL=Image.new("RGBA",img.size,(0,0,0,0)); glow=Image.new("RGBA",img.size,(0,0,0,0)); sh=Image.new("RGBA",img.size,(0,0,0,0))
    dt,dg,ds=ImageDraw.Draw(txtL),ImageDraw.Draw(glow),ImageDraw.Draw(sh)
    for k,ln in enumerate(lines):
        x=(W-FONT.getlength(" ".join(ln)))/2; y=20+k*LH
        for w in ln:
            c=COR.get(cm.get(w.strip(",.'«»:\"")),(255,255,255))
            dt.text((x,y),w,font=FONT,fill=c+(255,)); dg.text((x,y),w,font=FONT,fill=c+(200,))
            ds.text((x+2,y+3),w,font=FONT,fill=(0,0,0,230),stroke_width=3,stroke_fill=(0,0,0,230))
            x+=FONT.getlength(w+" ")
    out=Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)),glow.filter(ImageFilter.GaussianBlur(7)))
    out=Image.alpha_composite(out,txtL)
    return np.array(out).astype(np.float32)
for b in blocos: b.append(render(b[2],b[3],CENA(b[0]+0.05)))
# ---- seta
def seta_img():
    s=Image.new("RGBA",(110,150),(0,0,0,0)); d=ImageDraw.Draw(s)
    pts=[(40,10),(70,10),(70,85),(100,85),(55,140),(10,85),(40,85)]
    g=Image.new("RGBA",s.size,(0,0,0,0)); ImageDraw.Draw(g).polygon(pts,fill=(255,40,40,200))
    d.polygon(pts,fill=(235,20,20,255),outline=(255,255,255,255))
    return np.array(Image.alpha_composite(g.filter(ImageFilter.GaussianBlur(6)),s)).astype(np.float32)
SETA=seta_img(); T_SETA=26.65
def over(img,rgba,x,y):
    h,w=rgba.shape[:2]; y0,y1=max(0,y),min(H,y+h); x0,x1=max(0,x),min(W,x+w)
    if y1<=y0 or x1<=x0: return
    r=rgba[y0-y:y1-y,x0-x:x1-x]; a=r[...,3:4]/255.0
    img[y0:y1,x0:x1]=img[y0:y1,x0:x1]*(1-a)+r[...,2::-1]*a

enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-i","audio/mix_it.wav","-map","0:v","-map","1:a","-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
    "-c:v","libx264","-crf","16","-preset","medium","-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",OUT],stdin=subprocess.PIPE)
for n in range(N):
    t=n/FPS; nb=n if t<CUTS[1] else int(round((t-SHIFT)*FPS)); f=base[min(nb,len(base)-1)]
    for fr,a,b in hg:
        if a-1e-6<=t<b-1e-6:
            k=int(round((t-a)*FPS)); f=fr[min(k,len(fr)-1)]
    img=f.astype(np.float32)
    for b in blocos:
        if b[0]-0.03<=t<b[4]:
            r=b[5]; sc=min(1.0,0.85+0.15*(t-b[0]+0.03)/0.12)
            if sc<1: r=cv2.resize(r,None,fx=sc,fy=sc,interpolation=cv2.INTER_LINEAR)
            c_=CENA(t); xc=XC.get(c_,W/2)
            over(img,r,int(xc-r.shape[1]/2),int(YC[c_]-r.shape[0]/2))
    if t>=T_SETA:
        dy=int(-14*abs(np.sin(np.pi*(t-T_SETA)/0.55)))
        over(img,SETA,W//2-55,int(YC[6]-215+dy))
    enc.stdin.write(np.clip(img,0,255).astype(np.uint8).tobytes())
    if n%150==0: print(f"[{n}/{N}]",flush=True)
enc.stdin.close(); enc.wait(); print("ok",OUT)
json.dump([[round(b[0],2),round(b[4],2),b[2]] for b in blocos],open("blocos_it.json","w"),indent=0)

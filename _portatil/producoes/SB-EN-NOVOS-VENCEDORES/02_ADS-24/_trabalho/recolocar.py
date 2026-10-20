# base_en.mp4 + saidas HeyGen -> base_final.mp4 (cor bt601 fixa)
# modo full (heygen_out2): topo do quadro (rosto) do HeyGen, faixa da legenda (y>860) da base v2
# modo crop (heygen_out3): recorte 288x512 em (261,60) ampliado 2,5x -> reduz e cola so boca/queixo (elipse suave)
import json, os, subprocess, numpy as np, cv2
W,H=720,1280
def quadros(src):
    p=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-vf","scale=720:1280:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,fps=30,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3)
fr=[f.copy() for f in quadros("base_en.mp4")]
AL=np.clip((860-np.arange(H))/80,0,1).astype(np.float32)[:,None,None]
CX,CY,CW,CH=261,60,288,512
E=np.zeros((CH,CW),np.float32); cv2.ellipse(E,(405-CX,272-CY),(60,50),0,0,360,1,-1); E=cv2.GaussianBlur(E,(0,0),9)[...,None]
EXCL=[(5.96,6.46)]  # A1: dentes quadriculados do HeyGen logo apos o flash -> boca da base
CROP=set(json.load(open("crop.json"))) if os.path.exists("crop.json") else set()
for n,a,b in json.load(open("chunks.json")):
    i0=round(a*30); m=round(b*30)-i0
    if n in CROP:
        q=list(quadros(f"heygen_out3/{n}.mp4"))[:m]
        for j in range(m):
            k=min(j,len(q)-1); c=cv2.resize(q[k],(CW,CH),interpolation=cv2.INTER_AREA).astype(np.float32)
            reg=fr[i0+j][CY:CY+CH,CX:CX+CW].astype(np.float32)
            fr[i0+j][CY:CY+CH,CX:CX+CW]=np.clip(c*E+reg*(1-E),0,255).astype(np.uint8)
        print(n,"crop",len(q),m); continue
    p=f"heygen_out2/{n}.mp4" if os.path.exists(f"heygen_out2/{n}.mp4") else f"heygen_out5/{n}.mp4"
    if not os.path.exists(p): print("FALTA",n); continue
    q=list(quadros(p))
    if len(q)!=m: print(n,"quadros",len(q),"esperado",m)
    for j in range(m):
        k=min(j,len(q)-1)
        if any(e0<=(i0+j)/30<=e1 for e0,e1 in EXCL): continue
        fr[i0+j]=(q[k]*AL+fr[i0+j]*(1-AL)).astype(np.uint8)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-an",
  "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
  "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","smpte170m","base_final.mp4"],stdin=subprocess.PIPE)
for f in fr: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("ok",len(fr))

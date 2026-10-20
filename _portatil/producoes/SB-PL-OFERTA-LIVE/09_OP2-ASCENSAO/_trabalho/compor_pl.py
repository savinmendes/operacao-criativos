# Compõe o AD PL: gancho + corpo HeyGen PL, b-rolls limpos nas mesmas cenas do ES (crossfade 0,2 s, zoom lento,
# vinheta medida no AD ES), legenda ASS no estilo do ES, seta amarela, voz PL + trilha (demucs do ES).
import cv2, numpy as np, subprocess, json, sys
W,H,FPS=1080,1920,30
B=r"C:\Users\PICHAU\Downloads\SAN BENITO B-ROLS\\"
C=json.load(open("cortes_pl.json")); TOTAL=C[-1]; HK=C[1]
HOOK="heygen/hook_pl_heygen.mp4"; CORPO="heygen/corpo_pl_heygen.mp4"
# (fonte, tempo da fonte no inicio da cena = função)
seg=[(HOOK,lambda t:t),(CORPO,lambda t:t-HK),(B+"SB-BRV-55 MANO EN EL PECHO KLING25.mp4",None),
     (B+"SB-BRV-01 REGALO NOMBRE KLING25.mp4",None),(B+"SB-BRV-69 CATACUMBAS KLING25.mp4",None),
     (B+"SB-BRV-03 LLUVIA MILAGROS KLING25.mp4",None),("heygen/clipA_pl_heygen.mp4",lambda t:t-16.93),
     (B+"SB-BRV-30 SCROLL DETENIDO KLING25.mp4",None),("heygen/clipB_pl_heygen.mp4",lambda t:t-24.01)]
XF=0.10  # meia duração do crossfade
duro={1}  # fronteira 1 (gancho->corpo) é corte seco, como no ES
def decode(p,ss,dur):
    vf=f"scale={W}:{H}:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24"
    cmd=["ffmpeg","-v","error","-ss",f"{max(0,ss):.3f}","-i",p,"-t",f"{dur:.3f}","-vf",vf,"-fps_mode","passthrough","-f","rawvideo","-"]
    raw=subprocess.run(cmd,capture_output=True).stdout
    n=len(raw)//(W*H*3); fr=np.frombuffer(raw[:n*W*H*3],np.uint8).reshape(n,H,W,3)
    fps=cv2.VideoCapture(p).get(cv2.CAP_PROP_FPS)
    return fr,fps,max(0,ss)
cache={}
def frames_seg(i):
    if i in cache: return cache[i]
    p,fn=seg[i]; a=C[i]-(0 if i in duro or i==0 else XF); b=C[i+1]+(0 if (i+1) in duro or i==8 else XF)
    s0=fn(a) if fn else 0.0
    fr,fps,ss=decode(p,s0,b-a+0.2)
    if fn and s0<0: fr=np.concatenate([np.repeat(fr[:1],int(round(-s0*fps)),0),fr])
    cache[i]=(fr,fps,ss,a,s0); return cache[i]
def zoom(img,i,t):
    z=1.02+0.05*np.clip((t-C[i])/(C[i+1]-C[i]),0,1)
    cx,cy=W/2,H*0.47
    M=np.float32([[z,0,cx-z*cx],[0,z,cy-z*cy]])
    return cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
def quadro(i,t):
    fr,fps,ss,a,s0=frames_seg(i)
    k=int(round((t-a)*fps)); k=min(max(k,0),len(fr)-1)
    return zoom(fr[k],i,t).astype(np.float32)
# vinheta medida (razão AD ES / fonte por distância ao centro)
yy,xx=np.mgrid[0:H,0:W]; d=np.hypot(xx-W/2,yy-H/2)/np.hypot(W/2,H/2)
dp=[0,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.0]; gp=[1,1,0.99,0.93,0.88,0.81,0.74,0.67,0.55,0.43,0.33,0.30]
VIG=np.interp(d,dp,gp).astype(np.float32)[...,None]
N=int(round(TOTAL*FPS))
T7=C[7]
vf=(f"[0:v]ass=leg_pl.ass:fontsdir=fonts[l];[l][1:v]overlay=x=430:y='1561-28*sin(2*PI*(t-{T7})/0.558)':enable='gte(t,{T7})'[o];"
    "[o]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
     "-loop","1","-i","seta_amarela.png","-i","audio/mix_pl.wav","-filter_complex",vf,"-map","[v]","-map","2:a",
     "-c:v","libx264","-crf","14","-preset","medium","-r",str(FPS),"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}",
     "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
     "bruto_pl.mp4"],stdin=subprocess.PIPE)
for n in range(N):
    t=n/FPS
    i=max(k for k in range(9) if C[k]<=t+1e-6)
    img=quadro(i,t)
    if i>0 and i not in duro and t<C[i]+XF:
        al=(t-(C[i]-XF))/(2*XF); img=img*al+quadro(i-1,t)*(1-al)
    elif i<8 and (i+1) not in duro and t>=C[i+1]-XF:
        al=(t-(C[i+1]-XF))/(2*XF); img=quadro(i+1,t)*al+img*(1-al)
    img=np.clip(img*VIG,0,255).astype(np.uint8)
    enc.stdin.write(img.tobytes())
    for k in list(cache):
        if k<i-1: del cache[k]
    if n%60==0: print(f"[{n}/{N}] {100*n/N:.0f}%",flush=True)
enc.stdin.close(); enc.wait(); print("ok bruto_pl.mp4")

# Compõe o AD EN: base limpa (LaMa + patch do prédio) esticada ao tempo da narração, cartão EN, legenda ASS, seta no CTA, voz EN
import numpy as np, subprocess
W,H,FPS=1080,1920,30
NARR=137.741; TOTAL=round(NARR+0.25,2); SRC_DUR=136.9; NSRC=4107
TCTA=121.80
P=np.load("patch_v2.npy"); PA=2030
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/narracao_en.mp3","-af",f"loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{TOTAL}","-ar","48000","-ac","2","audio/voz_en.wav"],check=True)
dec=subprocess.Popen(["ffmpeg","-v","error","-i","base_limpa_v2.mp4","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
vf=("[0:v][1:v]overlay=0:0[c];[c]ass=leg_en.ass:fontsdir=fonts[l];"
    f"[l][2:v]overlay=x=430:y='1600-28*sin(2*PI*(t-{TCTA})/0.558)':enable='gte(t,{TCTA})'[o];"
    "[o]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-loop","1","-i","card_en.png","-loop","1","-i","seta_amarela.png","-i","audio/voz_en.wav","-filter_complex",vf,"-map","[v]","-map","3:a",
    "-c:v","libx264","-crf","18","-preset","medium","-r",str(FPS),"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
    "-movflags","+faststart","bruto_en.mp4"],stdin=subprocess.PIPE)
src=[]; k=0
while True:
    raw=dec.stdout.read(W*H*3)
    if len(raw)<W*H*3: break
    f=np.frombuffer(raw,np.uint8).reshape(H,W,3)
    if PA<=k<PA+len(P): f=P[k-PA]
    src.append(f); k+=1
N=int(round(TOTAL*FPS)); fac=len(src)/N
for n in range(N):
    enc.stdin.write(np.ascontiguousarray(src[min(len(src)-1,int(n*fac))]).tobytes())
enc.stdin.close(); enc.wait(); print("ok TOTAL",TOTAL,"fator",round(fac,4))

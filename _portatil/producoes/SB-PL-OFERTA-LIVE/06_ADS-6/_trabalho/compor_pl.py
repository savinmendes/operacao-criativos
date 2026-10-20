# Compõe o AD PL: base limpa EN (LaMa + patch do prédio, só leitura) esticada ao tempo da narração PL, cartão PL, legenda ASS, seta no CTA, voz PL
# Versão em streaming (não guarda os 4107 quadros na memória)
import numpy as np, subprocess
EN=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\06_ADS-6\_trabalho"
W,H,FPS=1080,1920,30
NARR=152.832; TOTAL=round(NARR+0.25,2); NSRC=4107
TCTA=135.42
P=np.load(EN+r"\patch_v2.npy",mmap_mode="r"); PA=2030
subprocess.run(["ffmpeg","-v","error","-y","-i","audio/narracao_pl.mp3","-af",f"loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{TOTAL}","-ar","48000","-ac","2","audio/voz_pl.wav"],check=True)
dec=subprocess.Popen(["ffmpeg","-v","error","-i",EN+r"\base_limpa_v2.mp4","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
vf=("[0:v][1:v]overlay=0:0[c];[c]ass=leg_pl.ass:fontsdir=fonts[l];"
    f"[l][2:v]overlay=x=430:y='1600-28*sin(2*PI*(t-{TCTA})/0.558)':enable='gte(t,{TCTA})'[o];"
    "[o]scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]")
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-loop","1","-i","card_pl.png","-loop","1","-i","seta_amarela.png","-i","audio/voz_pl.wav","-filter_complex",vf,"-map","[v]","-map","3:a",
    "-c:v","libx264","-crf","18","-preset","medium","-r",str(FPS),"-c:a","aac","-b:a","192k","-ar","48000","-t",f"{TOTAL:.3f}",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
    "-movflags","+faststart","bruto_pl.mp4"],stdin=subprocess.PIPE)
N=int(round(TOTAL*FPS)); fac=NSRC/N
k=-1; cur=None
for n in range(N):
    alvo=min(NSRC-1,int(n*fac))
    while k<alvo:
        raw=dec.stdout.read(W*H*3)
        if len(raw)<W*H*3: break
        k+=1
        cur=P[k-PA] if PA<=k<PA+len(P) else np.frombuffer(raw,np.uint8).reshape(H,W,3)
    enc.stdin.write(np.ascontiguousarray(cur).tobytes())
    if n%600==0: print(f"[{n}/{N}] {100*n//N}%",flush=True)
dec.stdout.close(); enc.stdin.close(); enc.wait(); print("ok TOTAL",TOTAL,"fator",round(fac,4),"ult src",k)

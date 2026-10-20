# v2: máscara com margem larga (elipse 61x41) e LaMa em meia resolução (evita blocos fantasma na borda do furo)
import sys, time, warnings, subprocess; warnings.filterwarnings("ignore")
import numpy as np, cv2
from teste_lama2 import limpar
from mascara2 import mascara
SRC=r"C:\Users\PICHAU\Downloads\SAN-BENITO-ES-VENCEDORES\SB-ES_02_ADS-6.mp4"
W,H=1080,1920; FPS=30; N=4107
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an",
    "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p","-c:v","libx264","-crf","12","-preset","medium",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1","base_limpa_v2.mp4"],stdin=subprocess.PIPE)
K=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(61,41)); i=0; t0=time.time()
while True:
    raw=dec.stdout.read(W*H*3)
    if len(raw)<W*H*3: break
    f=np.frombuffer(raw,np.uint8).reshape(H,W,3).copy()
    m=mascara(f)
    if m.any(): f=limpar(f,cv2.dilate(m,K),0.5)
    enc.stdin.write(f.tobytes()); i+=1
    if i%300==0: el=time.time()-t0; print(f"[{i}/{N}] {100*i//N}% falta ~{el/i*(N-i):.0f} s",flush=True)
enc.stdin.close(); enc.wait(); print("ok",i,round(time.time()-t0))

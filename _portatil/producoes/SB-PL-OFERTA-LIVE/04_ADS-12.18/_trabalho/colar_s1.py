# Cola a boca do HeyGen recortado (s1_crop_hg: crop 360x640 @ 360,400 do s1_in, ampliado 2x) de volta no quadro inteiro,
# com elipse suave em boca e queixo. Cor bt601/tv fixa na leitura e gravacao. -> heygen/s1_hg_final.mp4
import subprocess, numpy as np, cv2, sys
W,H,FPS=720,1280,30
def dec(p,w,h):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-vf",f"fps={FPS},scale={w}:{h}:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24","-f","rawvideo","-"],capture_output=True).stdout
    n=len(raw)//(w*h*3); return np.frombuffer(raw[:n*w*h*3],np.uint8).reshape(n,h,w,3)
base=dec("heygen_in/s1_in.mp4",W,H); cr=dec("heygen/s1_crop_hg.mp4",720,1280)
CX,CY,RX,RY=float(sys.argv[1]) if len(sys.argv)>1 else 555,float(sys.argv[2]) if len(sys.argv)>2 else 765,62,58
m=np.zeros((H,W),np.float32); cv2.ellipse(m,(int(CX),int(CY)),(RX,RY),0,0,360,1,-1); m=cv2.GaussianBlur(m,(0,0),10)[...,None]
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-vf",
    "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p","-c:v","libx264","-crf","12",
    "-bsf:v","h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
    "heygen/s1_hg_final.mp4"],stdin=subprocess.PIPE)
n=min(len(base),len(cr)); print("quadros",len(base),len(cr))
for i in range(n):
    f=base[i].astype(np.float32); c=cv2.resize(cr[i],(360,640),interpolation=cv2.INTER_AREA).astype(np.float32)
    big=f.copy(); big[400:1040,360:720]=c
    enc.stdin.write(np.clip(f*(1-m)+big*m,0,255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print("ok")

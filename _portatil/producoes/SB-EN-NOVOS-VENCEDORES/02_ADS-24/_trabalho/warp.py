# base_limpa (ES, 148 s) -> base_en.mp4 (linha do tempo EN), quadro mais proximo; cor bt601/tv fixa
import subprocess, numpy as np
from mapa import en2es, TOTAL
W,H=720,1280
def quadros(src):
    p=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3)
import sys
SRCV=sys.argv[1] if len(sys.argv)>1 else "base_limpa.mp4"; OUTV=sys.argv[2] if len(sys.argv)>2 else "base_en.mp4"
fr=list(quadros(SRCV)); N=round(TOTAL*30)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-an",
  "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
  "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","smpte170m",OUTV],stdin=subprocess.PIPE)
idx=[]
for n in range(N):
    k=min(len(fr)-1,max(0,int(round(en2es((n+0.5)/30)*30-0.5)))); idx.append(k); ff.stdin.write(fr[k].tobytes())
ff.stdin.close(); ff.wait(); np.save("warp_idx.npy",np.array(idx)); print("ok",N,len(fr))

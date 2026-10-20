# remove a barrinha verde (cursor do editor do original) ao lado da caixa do gancho, quadros 0-145
import subprocess, numpy as np, cv2
W,H=720,1280
p=subprocess.Popen(["ffmpeg","-v","error","-i","base_final.mp4","-vf","scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-an",
  "-vf","scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
  "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","smpte170m","base_final2.mp4"],stdin=subprocess.PIPE)
i=0; n=0
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).copy()
    if i<146:
        r=f[880:1080,480:700]; hsv=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
        m=((hsv[...,0]>=40)&(hsv[...,0]<=95)&(hsv[...,1]>=70)&(hsv[...,2]>=120)).astype(np.uint8)
        if m.sum()>20:
            m=cv2.dilate(m,np.ones((9,9),np.uint8)); f[880:1080,480:700]=cv2.inpaint(r,m,7,cv2.INPAINT_TELEA); n+=1
    ff.stdin.write(f.tobytes()); i+=1
ff.stdin.close(); ff.wait(); print("ok",i,"corrigidos",n)

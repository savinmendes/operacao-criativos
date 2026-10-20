import sys, subprocess, numpy as np, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
p=subprocess.run(["ffmpeg","-v","error","-i",r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4","-vf","fps=5,format=bgr24","-f","rawvideo","-"],capture_output=True).stdout
F=np.frombuffer(p,np.uint8).reshape(-1,1280,720,3)
det=cl.Rastreador(multi=True)
out=[]
for i,f in enumerate(F):
    out.append([list(map(int,r)) for r in det.todos_rostos(f.copy())])
json.dump(out,open("rostos5fps.json","w"))
prev=None
for i,fs in enumerate(out):
    big=max([f[2] for f in fs],default=0)
    tag=f"{len(fs)}f w{big//50*50}"
    if tag!=prev: print(f"{i/5:6.1f} {tag} {fs[:3]}"); prev=tag

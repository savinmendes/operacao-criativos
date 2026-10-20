import subprocess, numpy as np, json, cv2
O=r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"; B=r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\visual\base_sem_legenda.mp4"
def rd(p, rng):
    return subprocess.Popen(["ffmpeg","-v","error","-i",p,"-vf",f"scale=360:640:in_range={rng},format=gray","-f","rawvideo","-"],stdout=subprocess.PIPE)
a=rd(O,"full"); b=rd(B,"limited"); N=360*640; out=[]
k=0
while True:
    x=a.stdout.read(N); y=b.stdout.read(N)
    if len(x)<N or len(y)<N: break
    d=np.abs(np.frombuffer(x,np.uint8).astype(int)-np.frombuffer(y,np.uint8).astype(int)).reshape(640,360)
    m=(d>14).astype(np.uint8); m[:70]=0  # ignora título/moldura do topo
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    ys,xs=np.where(m>0)
    out.append(None if len(xs)<20 else [int(xs.min()*2),int(ys.min()*2),int(xs.max()*2+2),int(ys.max()*2+2),int(len(xs))])
    k+=1
json.dump(out,open("v2/difmask.json","w")); print(k)

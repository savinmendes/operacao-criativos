import sys,json,numpy as np,cv2,mediapipe as mp,soundfile as sf
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho")
from comum3 import quadros
v=r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\SB-EN-AVATAR-REST_v2.mp4"
segs=[(10.7,15.2),(17.07,22.35),(25.88,29.15),(35.06,37.49),(41.19,43.65),(47.71,50.18),(52.34,53.98)]
idx=set()
for a,b in segs: idx.update(range(round(a*30),round(b*30)))
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from pathlib import Path
det=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(Path.home()/'.cache'/'kit-edicao'/'face_landmarker.task')),running_mode=vision.RunningMode.IMAGE,num_faces=1))
x,sr=sf.read("audio.wav")
W=json.load(open("../palavras_en.json"))
out={};crops={}
for i,f in enumerate(quadros(v,w=1080,h=1920)):
    if i not in idx: continue
    rec=np.ascontiguousarray(cv2.cvtColor(f[:1080],cv2.COLOR_BGR2RGB))
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=rec))
    if not r.face_landmarks: out[i]=None;continue
    L=r.face_landmarks[0]
    p=lambda k:np.array([L[k].x*1080,L[k].y*1080])
    ab=np.linalg.norm(p(13)-p(14)); fh=np.linalg.norm(p(10)-p(152)); lw=np.linalg.norm(p(61)-p(291))
    c=(p(13)+p(14))/2
    out[i]=[ab/fh,lw/fh,float(c[0]),float(c[1]),fh]
    t=i/30; s=x[int(t*sr):int((t+1/30)*sr)]
    out[i].append(float(20*np.log10(np.sqrt(np.mean(s**2))+1e-9)))
    fala=any(w[1]-0.03<=t<=w[2]+0.03 for w in W)
    out[i].append(fala)
    cx,cy=int(c[0]),int(c[1]); hh=int(fh*0.28)
    crops[i]=cv2.resize(f[max(0,cy-hh):cy+hh,max(0,cx-int(hh*1.4)):cx+int(hh*1.4)],(336,240))
json.dump(out,open("boca.json","w"))
np.save("boca_crops.npy",{k:v for k,v in crops.items()},allow_pickle=True)

import os, subprocess, json, numpy as np, cv2
from pathlib import Path
os.environ["GLOG_minloglevel"]="2"
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
M = Path.home()/".cache"/"kit-edicao"/"face_landmarker.task"
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(M)), running_mode=vision.RunningMode.IMAGE, num_faces=4))
raw = subprocess.run(["ffmpeg","-v","error","-i","../../02_331k_DR0OM-REWzS.mp4","-t","7.2","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
F = np.frombuffer(raw,np.uint8).reshape(-1,1280,720,3)
out=[]
for i,f in enumerate(F):
    res=[]
    for (x0,y0,L) in ((80,200,520),(0,150,720)):
        rec=np.ascontiguousarray(f[y0:y0+L,x0:x0+L])
        r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=rec))
        for lm in (r.face_landmarks or []):
            p=np.array([(x0+q.x*L,y0+q.y*L) for q in lm]); res.append([float(p[:,0].min()),float(p[:,1].min()),float(p[:,0].max()),float(p[:,1].max()), float(p[[13,14],0].mean()), float(p[[13,14],1].mean())])
        if res: break
    out.append(res)
    if i%8==0: print(f"{i/30:.2f}", [[int(v) for v in b] for b in res])
json.dump(out,open("lipsync/rostos.json","w"))

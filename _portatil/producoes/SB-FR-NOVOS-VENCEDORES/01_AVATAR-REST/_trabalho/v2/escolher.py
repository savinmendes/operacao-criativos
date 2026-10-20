import cv2, numpy as np, mediapipe as mp, sys
sys.path.insert(0,'..')
from comum3 import quadros
from pathlib import Path
MOD=str(Path.home()/".cache"/"kit-edicao"/"face_landmarker.task")
det=mp.tasks.vision.FaceLandmarker.create_from_options(mp.tasks.vision.FaceLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=MOD),num_faces=1))
SRC="C:/Users/PICHAU/Downloads/1-VIDEOS/AVATAR_REST.mp4"
INT=[(37.1,40.7),(45.9,48.75),(52.567,54.77),(61.833,64.5),(66.333,68.7)]
res=[]
for k,f in enumerate(quadros(SRC,w=1080,h=1920)):
    t=k/30
    if not any(a<=t<b for a,b in INT): continue
    if k%2: continue
    r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))))
    if not r.face_landmarks: continue
    p=np.array([(q.x*1080,q.y*1920) for q in r.face_landmarks[0]])
    fw=np.linalg.norm(p[234]-p[454]); op=np.linalg.norm(p[13]-p[14])/fw
    yaw=((p[1][0]-p[234][0])/(p[454][0]-p[234][0]))-0.5
    mw=np.linalg.norm(p[61]-p[291])/fw
    res.append((op,abs(yaw),mw,t,k)); 
res.sort()
for x in res[:25]: print("op %.4f yaw %.3f mw %.3f t %.2f k %d"%x)

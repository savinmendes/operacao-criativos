import cv2,numpy as np,mediapipe as mp,os,sys
from mediapipe.tasks.python import vision, BaseOptions
opt=vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=os.path.expanduser('~/.cache/kit-edicao/face_landmarker.task')),num_faces=1)
det=vision.FaceLandmarker.create_from_options(opt)
segs=[(1,840),(2,1116),(3,1317),(4,1517),(5,1667)]
for k,f0 in segs:
    cap=cv2.VideoCapture(f'ls/p{k}.mp4'); i=0; out=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)))
        if r.face_landmarks:
            L=r.face_landmarks[0]; h,w=f.shape[:2]
            op=abs(L[13].y-L[14].y)*h; fw=abs(L[234].x-L[454].x)*w
            out.append(op/fw*100)
        else: out.append(np.nan)
        i+=1
    s=' '.join(f'{(f0+j)/30:.2f}:{v:.1f}' for j,v in enumerate(out))
    print('P',k); print(s)

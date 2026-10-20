import sys, os, json; os.environ["GLOG_minloglevel"]="2"
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from segs import SEGS
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
cap = cv2.VideoCapture("../base_sem_legenda.mp4"); out = {}
for k,(a,b) in enumerate(SEGS,1):
    W=[];J=[]
    for q in range(a,b+1,6):
        cap.set(1,q); ok,f=cap.read()
        r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))))
        ps=[np.array([(p.x*720,p.y*1280) for p in fl]) for fl in r.face_landmarks]
        bx=[(p[:,0].min(),p[:,1].min(),p[:,0].max(),p[:,1].max()) for p in ps]
        bx.sort(key=lambda t:t[0])
        if len(bx)>=2: J.append(bx[0]); W.append(bx[-1])
        elif len(bx)==1: W.append(bx[0])
    W=np.array(W); J=np.array(J) if J else np.zeros((0,4))
    o={"w":[float(W[:,0].min()),float(W[:,1].min()),float(W[:,2].max()),float(W[:,3].max())],
       "j":[float(J[:,0].min()),float(J[:,1].min()),float(J[:,2].max()),float(J[:,3].max())] if len(J) else None,"nj":len(J),"n":len(W)}
    out[f"s{k:02d}"]=o; print(k,a,b,{x:(np.round(v).astype(int).tolist() if isinstance(v,list) else v) for x,v in o.items()},flush=True)
json.dump(out,open("rostos.json","w"),indent=1)

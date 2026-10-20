import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())),
    running_mode=vision.RunningMode.IMAGE, num_faces=2, min_face_detection_confidence=0.2, min_face_presence_confidence=0.2))
cap = cv2.VideoCapture("../../../../UNICOS_HD/10.mp4")
x0,y0,x1,y1 = [int(v) for v in sys.argv[2].split(",")]
for a,b in [map(int,s.split("-")) for s in sys.argv[1].split(",")]:
    ok_n=0; tot=0
    for k in range(a,b,6):
        cap.set(cv2.CAP_PROP_POS_FRAMES,k); ok,f=cap.read(); c=f[y0:y1,x0:x1]; c=cv2.resize(c,None,fx=2,fy=2)
        c=cv2.convertScaleAbs(c, alpha=1.0, beta=0)
        r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB))))
        tot+=1; ok_n+= len(r.face_landmarks)>0
    print(a,b,ok_n,"/",tot)

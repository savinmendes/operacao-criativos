import sys, os, json
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=4,
    min_face_detection_confidence=0.3))
src=sys.argv[1]; segs=json.loads(sys.argv[2])  # [[nome,a,b],...]
cap=cv2.VideoCapture(src); fr={}
need=set()
for n,a,b in segs: need|=set(range(a,b,6))
i=0
while True:
    ok,f=cap.read()
    if not ok: break
    if i in need: fr[i]=f
    i+=1
res={}
for n,a,b in segs:
    F=[]
    for k in range(a,b,6):
        f=fr[k]; r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))))
        F.append([[round(float(p[:,0].min())),round(float(p[:,1].min())),round(float(p[:,0].max())),round(float(p[:,1].max())),round(float(p[13][0])),round(float(p[13][1]))] for p in [np.array([(q.x*720,q.y*1280) for q in fl]) for fl in r.face_landmarks]])
    nf=[len(x) for x in F]
    print(n,a,b,'faces/quadro',min(nf),max(nf))
    allf=[x for fs in F for x in fs]
    if allf:
        A=np.array(allf); print('   boxes x0',A[:,0].min(),'y0',A[:,1].min(),'x1',A[:,2].max(),'y1',A[:,3].max(),'boca y',A[:,5].min(),A[:,5].max())
        # list distinct by mouth position
        for fs in F[::max(1,len(F)//3)]: print('   ',fs)
    res[n]=F
json.dump(res,open(sys.argv[3],'w'))

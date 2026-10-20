import sys, cv2, numpy as np
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1))
def ab(p):
    c=cv2.VideoCapture(p); out=[]
    while True:
        ok,f=c.read()
        if not ok: break
        f=np.ascontiguousarray(f[285:545,85:368]); H,W=f.shape[:2]
        r=det.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(f,cv2.COLOR_BGR2RGB)))
        out.append(cl._abertura(np.array([(q.x*W,q.y*H) for q in r.face_landmarks[0]])) if r.face_landmarks else np.nan)
    return np.array(out)
a=ab("_rev_cor/cmp/w04_antes.mp4"); b=ab("_rev_cor/cmp/w04_novo.mp4")
x=cl.ler_audio("lipsync3/rev/es_w04.mp3"); env=cl.envelope(x,16000,30,len(a)); fal=cl.mascara_fala(env)
d=b-a
P=[k for k in range(len(a)) if not fal[k] and abs(np.nan_to_num(d[k]))>0.004]
print([(1003+k, round(a[k],3), round(b[k],3)) for k in P])
print("pausas:", [1003+k for k in range(len(a)) if not fal[k]][:80])

import sys, json, cv2, numpy as np, mediapipe as mp
from pathlib import Path
from mediapipe.tasks.python import vision, BaseOptions
M=str(Path.home()/".cache"/"kit-edicao"/"face_landmarker.task")
lm=vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=M),num_faces=3))
d=json.load(open(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\voz\lotes.json",encoding="utf-8"))
cap=cv2.VideoCapture(r"C:\Users\PICHAU\Downloads\Lead 2.mp4")
out={}
for x in d["trechos"]:
    if x["lote"]!=2: continue
    if len(sys.argv)>1 and x["cena"]!=sys.argv[1]: continue
    bxs=[]
    for f in np.linspace(0.05,0.95,6):
        t=x["orig_ini"]+f*(x["orig_fim"]-x["orig_ini"])
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,im=cap.read()
        r=lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)))
        H,W=im.shape[:2]
        for fl in r.face_landmarks:
            xs=[p.x*W for p in fl]; ys=[p.y*H for p in fl]
            bxs.append([int(min(xs)),int(min(ys)),int(max(xs)),int(max(ys))])
    b=np.array(bxs) if bxs else None
    out[x["id"]]={"n":len(bxs),"x0":int(b[:,0].min()),"y0":int(b[:,1].min()),"x1":int(b[:,2].max()),"y1":int(b[:,3].max()),"w":int((b[:,2]-b[:,0]).mean())} if bxs else None
    print(x["id"],x["cena"],out[x["id"]],flush=True)
json.dump(out,open("rostos_%s.json"%(sys.argv[1] if len(sys.argv)>1 else "todos"),"w"),indent=1)

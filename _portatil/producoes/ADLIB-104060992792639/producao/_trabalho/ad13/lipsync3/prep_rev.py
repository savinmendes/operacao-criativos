# -*- coding: utf-8 -*-
"""Recorta os 14 trechos de rosto falando do VIDEO FINAL (rev/fin_<seg>.mp4 + ES do trecho) para o revisar_ad --lipsync,
com o original PT e a caixa do rosto de quem fala. Grava rev/spec.txt."""
import os, sys, json, subprocess, numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
FINAL = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 13 - ORACION-PAZ-ES-LATAM.mp4"
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())),
    running_mode=vision.RunningMode.IMAGE, num_faces=3, min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))
seg = json.loads((AD / "segmentos.json").read_text(encoding="utf-8"))["segmentos"]
V3 = {s["nome"] for s in json.loads((AQ / "segs.json").read_text())["segs"]}
NF = 3594; parts = []
(AQ / "rev").mkdir(exist_ok=True)
for s in seg:
    nm = Path(s["arquivo"]).stem.replace("seg_", ""); a, b = s["quadro_ini"], min(s["quadro_fim"] + 1, NF); t0, t1 = a / 30, b / 30
    fin = AQ / "rev" / f"fin_{nm}.mp4"; es = AQ / "rev" / f"es_{nm}.mp3"
    subprocess.run(["ffmpeg","-v","error","-y","-i",FINAL,"-vf",f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS","-an","-c:v","libx264","-crf","14","-threads","4",str(fin)], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",f"atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS","-ac","1","-c:a","libmp3lame","-b:a","192k",str(es)], check=True)
    if nm in V3:
        pt = AQ / "in" / f"orig_{nm}.mp4"; ro = (AQ / f"rosto_{nm}.txt").read_text().strip()
    else:
        pt = AD / "lipsync" / f"pt_{nm}.mp4"
        cap = cv2.VideoCapture(str(fin)); n = int(cap.get(7)); B = []
        for k in np.linspace(0, n - 1, 15).astype(int):
            cap.set(1, int(k)); ok, f = cap.read()
            r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
            fs = [np.array([(p.x * 720, p.y * 1280) for p in fl]) for fl in r.face_landmarks]
            if nm != "j1": fs = [p for p in fs if p[:, 0].mean() < 380] or fs
            if fs:
                p = max(fs, key=lambda p: np.ptp(p[:, 0])); B.append([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()])
        B = np.array(B); x0, y0 = np.percentile(B[:, 0], 5), np.percentile(B[:, 1], 5); x1, y1 = np.percentile(B[:, 2], 95), np.percentile(B[:, 3], 95)
        ro = f"{int(x0-20)},{int(y0-20)},{int(x1-x0+40)},{int(y1-y0+40)}"
    parts.append(f"{fin}:{es}:{pt}:{ro.replace(',', ';')}"); print(nm, a, b, ro, flush=True)
(AQ / "rev" / "spec.txt").write_text(",".join(parts), encoding="utf-8")

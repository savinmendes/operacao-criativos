# -*- coding: utf-8 -*-
"""Revisor (lote B): varre o video FINAL inteiro, quadro a quadro, e para CADA rosto achado mede a abertura da boca
no final e no original (mesmo tempo, mapeado), a diferenca de pixels na boca e na testa (controle).
Nao escolhe o personagem aqui: a escolha de quem fala e feita depois (analisar.py), por trecho.
Uso: python varrer.py NN  -> faces_NN.jsonl"""
import sys, json, os
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

NN = sys.argv[1]
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = next((P / "producao").glob(f"AD {NN} - *-ES-LATAM.mp4"))
ORI = P / "UNICOS_HD" / f"{NN}.mp4"


def mapa(t):
    """lote B: tempo do final = tempo do original (conferido com alinh.py)"""
    return t


opts = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())),
                                    running_mode=vision.RunningMode.IMAGE, num_faces=3)
det = vision.FaceLandmarker.create_from_options(opts)


def detect(fr, x0, y0, lado):
    h, w = fr.shape[:2]
    x1, y1 = min(w, x0 + lado), min(h, y0 + lado)
    rec = np.ascontiguousarray(cv2.cvtColor(fr[y0:y1, x0:x1], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec))
    rh, rw = rec.shape[:2]
    return [np.array([(x0 + p.x * rw, y0 + p.y * rh) for p in fl]) for fl in r.face_landmarks]


def larg(p):
    return float(np.linalg.norm(p[cl.ROSTO_LARG[0]] - p[cl.ROSTO_LARG[1]]))


def todos(fr):
    c = []
    for y0 in (0, 280, 560):
        c += detect(fr, 0, y0, 720)
    out = []
    for p in c:
        if larg(p) < 40: continue
        if all(np.linalg.norm(p[13] - q[13]) > 0.3 * larg(q) for q in out): out.append(p)
    return out


def perto(fr, ref):
    L = larg(ref); lado = int(min(720, max(200, 3 * L))); cx, cy = ref[13]
    x0 = int(np.clip(cx - lado / 2, 0, 720 - lado)); y0 = int(np.clip(cy - lado / 2, 0, 1280 - lado))
    c = detect(fr, x0, y0, lado)
    if not c: return None
    p = min(c, key=lambda q: np.linalg.norm(q[13] - ref[13]))
    return p if np.linalg.norm(p[13] - ref[13]) < 0.5 * L else None


cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI))
fpo = co.get(cv2.CAP_PROP_FPS)
oi, o = -1, None
out = open(Path(__file__).parent / f"faces_{NN}.jsonl", "w")
k = 0
while True:
    ok, f = cf.read()
    if not ok: break
    want = int(round(mapa(k / 30) * fpo))
    while oi < want:
        ok2, o2 = co.read()
        if not ok2: break
        o = o2; oi += 1
    faces = []
    for p in todos(f):
        r = {"cx": int(p[13][0]), "cy": int(p[13][1]), "L": round(larg(p), 1), "ab_f": round(cl._abertura(p), 4)}
        if o is not None:
            po = perto(o, p)
            cb = cl._caixa(p, cl.LABIOS_EXT, 0.35, f.shape)
            r["d_boca"] = round(cl._dif(f, o, cb), 2)
            r["d_ctrl"] = round(cl._dif(f, o, cl._caixa_testa(p, f.shape)), 2)
            if po is not None: r["ab_o"] = round(cl._abertura(po), 4)
        faces.append(r)
    out.write(json.dumps({"q": k, "faces": faces}) + "\n")
    k += 1
    if k % 300 == 0: print(k, flush=True)
out.close()
print("ok", k)

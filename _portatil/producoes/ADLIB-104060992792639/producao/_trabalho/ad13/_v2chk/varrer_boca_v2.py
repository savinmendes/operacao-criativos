# -*- coding: utf-8 -*-
"""Revisor: varre o video final inteiro contra o original, quadro a quadro, medindo a boca DO PERSONAGEM QUE FALA
(os planos tem 2 rostos: o checar_lipsync do kit pega o rosto maior, que pode ser o personagem calado).
Regra de escolha: ad01 = rosto mais baixo (a mulher, na frente); ad13 = Jesus no j1 (0-197, rosto maior no inicio e
depois continuidade), mulher (rosto mais a esquerda) no resto.
Uso: python varrer_boca.py ad01|ad13  -> boca_adNN.csv"""
import sys, csv, os
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

AD = "ad13"
FAIXAS = [(211,455),(692,873),(1003,1307),(2285,2517),(2667,2949)]
den = lambda k: any(a <= k < b for a, b in FAIXAS)
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = P / "producao" / {"ad01": "AD 01 - ORACION-TRES-BENDICIONES-ES-LATAM.mp4", "ad13": "AD 13 - ORACION-PAZ-ES-LATAM.mp4", "ad11": "AD 11 - ORACION-DESATADORA-ES-LATAM.mp4"}[AD]
ORI = P / "UNICOS_HD" / {"ad01": "01.mp4", "ad13": "13.mp4", "ad11": "11.mp4"}[AD]
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
    for y0 in (0, 320, 640):          # meia largura: rostos menores
        for x0 in (0, 360):
            c += detect(fr, x0, y0, 360)
    out = []
    for p in c:                        # tira duplicados (mesma boca)
        if larg(p) < 25: continue
        if all(np.linalg.norm(p[13] - q[13]) > 0.3 * larg(q) for q in out): out.append(p)
    return out


def perto(fr, ref):
    """landmarks no quadro fr do rosto mais proximo da boca ref (recorte em volta)."""
    L = larg(ref); lado = int(min(720, max(160, 3 * L))); cx, cy = ref[13]
    x0 = int(np.clip(cx - lado / 2, 0, 720 - lado)); y0 = int(np.clip(cy - lado / 2, 0, 1280 - lado))
    c = detect(fr, x0, y0, lado)
    if not c: return None
    p = min(c, key=lambda q: np.linalg.norm(q[13] - ref[13]))
    return p if np.linalg.norm(p[13] - ref[13]) < 0.5 * L else None


cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI))
rows, prev_f, sel_prev = [], None, None
k = 0
while True:
    ok, f = cf.read()
    if not ok: break
    ok2, o = co.read()
    if not ok2: break
    if not den(k):
        prev_f = f; k += 1; continue
    cand = todos(o)
    sel = None
    if cand:
        if AD == "ad11":
            sel = max(cand, key=larg)
        elif AD == "ad01":
            sel = max(cand, key=lambda p: p[13][1])
        elif k <= 197:
            if sel_prev is not None:
                q = min(cand, key=lambda p: np.linalg.norm(p[13] - sel_prev[13]))
                sel = q if np.linalg.norm(q[13] - sel_prev[13]) < 0.6 * larg(sel_prev) else max(cand, key=larg)
            else:
                sel = max(cand, key=larg)
        else:
            sel = min(cand, key=lambda p: p[13][0])
    r = {"q": k, "t": round(k / 30, 3), "nrostos": len(cand)}
    if sel is not None:
        cb = cl._caixa(sel, cl.LABIOS_EXT, 0.35, f.shape)
        r.update(cx=int(sel[13][0]), cy=int(sel[13][1]), larg=round(larg(sel), 1),
                 d_boca=round(cl._dif(f, o, cb), 2), d_ctrl=round(cl._dif(f, o, cl._caixa_testa(sel, f.shape)), 2),
                 ab_o=round(cl._abertura(sel), 4))
        if prev_f is not None: r["d_prev"] = round(cl._dif(f, prev_f, cb), 2)
        pf = perto(f, sel)
        if pf is not None: r["ab_f"] = round(cl._abertura(pf), 4)
    rows.append(r); prev_f = f; sel_prev = sel; k += 1
    if k % 300 == 0: print(k, flush=True)
keys = ["q", "t", "nrostos", "cx", "cy", "larg", "d_boca", "d_ctrl", "d_prev", "ab_f", "ab_o"]
with open(Path(__file__).parent / "boca_v2.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, keys); w.writeheader()
    for r in rows: w.writerow({kk: r.get(kk, "") for kk in keys})
print("ok", k)

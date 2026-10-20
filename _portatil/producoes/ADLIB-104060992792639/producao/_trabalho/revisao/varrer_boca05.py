# -*- coding: utf-8 -*-
"""Revisor AD 05: final (30 fps, tempo novo) x original 05.mp4 (24 fps). Tempo novo t -> original t (t < 53,583)
ou t + 2,9167 (corte de 70 quadros a partir do quadro 1286). Mede a boca de QUEM FALA em cada bloco:
c1 = Clara (rosto mais alto do quadro; o marido sentado embaixo), m* = marido (rosto maior), c2/c3 = Clara (maior),
d* = Desatadora (rosto maior). Fora dos blocos: rosto maior. Saida: boca_ad05.csv (mesmas colunas + bloco)."""
import sys, csv, os, json
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
FIN = P / "producao" / "AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
ORI = P / "UNICOS_HD" / "05.mp4"
BL = json.loads((P / "producao/_trabalho/ad05/lipsync/blocos.json").read_text(encoding="utf-8"))
USADOS = ["c1", "m1", "c2", "c3", "m3", "m4", "m5", "d1", "d2", "d3", "d4", "d5"]
BL = [b for b in BL if b["id"] in USADOS]
COB = json.loads((P / "producao/_trabalho/ad05/lipsync/cobrir.json").read_text())
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=4))

def detect(fr, x0, y0, lado):
    h, w = fr.shape[:2]; x1, y1 = min(w, x0 + lado), min(h, y0 + lado)
    rec = np.ascontiguousarray(cv2.cvtColor(fr[y0:y1, x0:x1], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rec)); rh, rw = rec.shape[:2]
    return [np.array([(x0 + p.x * rw, y0 + p.y * rh) for p in fl]) for fl in r.face_landmarks]
larg = lambda p: float(np.linalg.norm(p[cl.ROSTO_LARG[0]] - p[cl.ROSTO_LARG[1]]))
def todos(fr):
    c = []
    for y0 in (0, 280, 560): c += detect(fr, 0, y0, 720)
    for y0 in (0, 320, 640):
        for x0 in (0, 360): c += detect(fr, x0, y0, 360)
    out = []
    for p in c:
        if larg(p) < 25: continue
        if all(np.linalg.norm(p[13] - q[13]) > 0.3 * larg(q) for q in out): out.append(p)
    return out
def perto(fr, ref):
    L = larg(ref); lado = int(min(720, max(160, 3 * L))); cx, cy = ref[13]
    x0 = int(np.clip(cx - lado / 2, 0, 720 - lado)); y0 = int(np.clip(cy - lado / 2, 0, 1280 - lado))
    c = detect(fr, x0, y0, lado)
    if not c: return None
    p = min(c, key=lambda q: np.linalg.norm(q[13] - ref[13]))
    return p if np.linalg.norm(p[13] - ref[13]) < 0.5 * L else None

def bloco(tn):
    q = tn * 24
    for b in BL:
        if b["a"] <= q < b["b"]: return b["id"]
    for a, b, _ in COB:
        if a <= q < b: return "COBERTO"
    return ""

cf, co = cv2.VideoCapture(str(FIN)), cv2.VideoCapture(str(ORI))
oi, of = -1, None
rows, prev_f, k = [], None, 0
while True:
    ok, f = cf.read()
    if not ok: break
    tn = k / 30
    to = tn if tn * 24 < 1286 else tn + 70 / 24
    want = int(round(to * 24))
    while oi < want:
        ok2, of = co.read(); oi += 1
    o = of
    b = bloco(tn)
    cand = todos(o)
    sel = None
    if cand:
        if b == "c1": sel = min(cand, key=lambda p: p[13][1])
        else: sel = max(cand, key=larg)
    r = {"q": k, "t": round(tn, 3), "bloco": b, "nrostos": len(cand)}
    if sel is not None and b != "COBERTO":
        cb = cl._caixa(sel, cl.LABIOS_EXT, 0.35, f.shape)
        r.update(cx=int(sel[13][0]), cy=int(sel[13][1]), larg=round(larg(sel), 1),
                 d_boca=round(cl._dif(f, o, cb), 2), d_ctrl=round(cl._dif(f, o, cl._caixa_testa(sel, f.shape)), 2),
                 ab_o=round(cl._abertura(sel), 4))
        if prev_f is not None: r["d_prev"] = round(cl._dif(f, prev_f, cb), 2)
        pf = perto(f, sel)
        if pf is not None: r["ab_f"] = round(cl._abertura(pf), 4)
    rows.append(r); prev_f = f; k += 1
keys = ["q", "t", "bloco", "nrostos", "cx", "cy", "larg", "d_boca", "d_ctrl", "d_prev", "ab_f", "ab_o"]
with open(Path(__file__).parent / "boca_ad05.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, keys); w.writeheader()
    for r in rows: w.writerow({kk: r.get(kk, "") for kk in keys})
print("ok", k)

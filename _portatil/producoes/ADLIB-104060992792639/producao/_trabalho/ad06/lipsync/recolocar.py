# -*- coding: utf-8 -*-
"""Recoloca os trechos de lipsync (out/ls_<n>.mp4 = recorte 9:16 escalado p/ 720x1280) na base_sem_legenda.mp4.
- Usa só os n quadros reais do trecho (descarta o enchimento); se vierem menos, REAMOSTRA no tempo (interpolação).
- --pula n=k descarta os k primeiros quadros da saída (quadro solto de outra tomada).
- Cola só a parte de baixo do rosto (elipse suave do nariz ao queixo), seguindo a boca quadro a quadro (MediaPipe na saída).
- Trechos que se sobrepõem (mesma tomada): crossfade linear na sobreposição.
- plano.json opcional: {"n": "out/arquivo.mp4"} troca a saída usada; {"cobrir": {"n": [x,y,w,h]}} cobre a boca com um
  enquadramento do próprio quadro (zoom no retângulo) em vez de lipsync.
Saída: ../base_lipsync.mp4 (bt709 tv) e out/full_<n>.mp4 (trecho colado, p/ medir)."""
import sys, os, json, subprocess
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AQ = Path(__file__).parent; AD = AQ.parent
cfg = json.loads((AQ/"segs.json").read_text()); FPS = cfg["fps"]; NTOT = cfg["ntot"]
plano = json.loads((AQ/"plano.json").read_text()) if (AQ/"plano.json").exists() else {}
pula = dict(a.split("=") for a in sys.argv[1:] if "=" in a)
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1,
    min_face_detection_confidence=0.3))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def ler(p):
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i*(m-1)/(n-1); j = int(np.floor(x)); a = x-j
        out.append(fr[-1] if j >= m-1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1-a, fr[j+1], a, 0)))
    return out
YY, XX = np.mgrid[0:1280, 0:720].astype(np.float32)
def elipse(cx, cy, ax, ay, sig):
    m = (((XX-cx)/ax)**2 + ((YY-cy)/ay)**2 <= 1).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), sig)[..., None]
def por(g, x, y, w, h):
    W, H = max(1, int(round(w))), max(1, int(round(h)))
    g2 = cv2.resize(g, (W, H), interpolation=cv2.INTER_AREA)
    return cv2.warpAffine(g2, np.float32([[w/W, 0, x], [0, h/H, y]]), (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
def colar_seg(s, bases, outs):
    if "track" in s: BX = json.load(open(AQ/f"boxes_{s['n']}.json"))
    else: BX = [s["crop"]]*len(bases)
    res = []; par = None
    for (x, y, w, h), b, g in zip(BX, bases, outs):
        sx, sy = w/720, h/1280
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB))))
        if r.face_landmarks:
            p = np.array([(q.x*720*sx + x, q.y*1280*sy + y) for q in r.face_landmarks[0]])
            fw = p[454,0]-p[234,0]; nose = p[1]; chin = p[152]; mo = (p[13]+p[14])/2
            novo = np.array([mo[0], (nose[1]+chin[1])/2 + 0.05*(chin[1]-nose[1]), 0.40*abs(fw), 0.70*(chin[1]-nose[1])])
            par = novo if par is None else 0.6*novo + 0.4*par
        if par is None:
            res.append(None); continue
        full = por(g, x, y, w, h)
        M = elipse(par[0], par[1], max(par[2], 20), max(par[3], 20), max(4, 0.07*abs(par[2])*2.5))
        res.append(np.clip(full*M + b*(1-M), 0, 255).astype(np.uint8))
    # quadros iniciais sem rosto detectado: usa a 1a elipse válida
    if par is not None:
        primeiro = next(i for i, v in enumerate(res) if v is not None)
        for i in range(primeiro):
            g = outs[i]; b = bases[i]; x, y, w, h = BX[i]
            full = por(g, x, y, w, h)
            M = elipse(par[0], par[1], max(par[2], 20), max(par[3], 20), 6)
            res[i] = np.clip(full*M + b*(1-M), 0, 255).astype(np.uint8)
    return [v if v is not None else b for v, b in zip(res, bases)]
def cobrir(bases, r):
    """r = [x,y,w,h] (zoom no próprio quadro) ou [x,y,w,h,q0] (zoom em quadros da mesma cena a partir de q0, ex. antes das setas)."""
    x, y, w, h = r[:4]
    if len(r) > 4:
        c = cv2.VideoCapture(str(AD/"base_sem_legenda.mp4")); c.set(1, r[4]); src = []
        for _ in bases:
            ok, f = c.read(); src.append(f)
        bases = src
    return [cv2.resize(b[y:y+h, x:x+w], (720, 1280), interpolation=cv2.INTER_LANCZOS4) for b in bases]
# lê a base inteira (2,5k quadros cabem na memória? 2,7 MB cada -> ~7 GB: não). Processa em streaming por trecho.
base = cv2.VideoCapture(str(AD/"base_sem_legenda.mp4"))
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD/"base_lipsync.mp4")], stdin=subprocess.PIPE)
segs = sorted(cfg["segs"], key=lambda s: s["a"])
proc = {}   # quadro -> imagem (só dentro dos trechos), liberado ao escrever
i = 0; buf = {}
def base_q(k):
    global i
    while i <= k:
        ok, f = base.read(); buf[i] = f; i += 1
    return buf[k]
escrito = 0
for idx, s in enumerate(segs):
    a, b, n = s["a"], s["b"], s["b"]-s["a"]
    bases = [base_q(k) for k in range(a, b)]
    if s["n"] in plano.get("cobrir", {}):
        fr = cobrir(bases, plano["cobrir"][s["n"]]); tipo = "coberto"
    else:
        arq = AQ/plano.get(s["n"], f"out/ls_{s['n']}.mp4")
        outs = ler(arq); k0 = int(pula.get(s["n"], 0)); outs = outs[k0:]
        m_total = len(outs); outs = outs[:n] if len(outs) >= n else reamostrar(outs, n)
        fr = colar_seg(s, bases, outs); tipo = f"lipsync {arq.name} {m_total}q->{n}"
    # trecho medido
    sub = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-c:v","libx264","-crf","14","-pix_fmt","yuv420p",str(AQ/"out"/f"full_{s['n']}.mp4")], stdin=subprocess.PIPE)
    for f in fr: sub.stdin.write(f.tobytes())
    sub.stdin.close(); sub.wait()
    for j, k in enumerate(range(a, b)):
        if k in proc:   # sobreposição: crossfade linear
            ov = [q for q in range(a, b) if q in proc]; t = (ov.index(k)+1)/(len(ov)+1)
            proc[k] = np.clip(proc[k].astype(np.float32)*(1-t) + fr[j].astype(np.float32)*t, 0, 255).astype(np.uint8)
        else: proc[k] = fr[j]
    print(s["n"], tipo, flush=True)
    # escreve tudo antes do próximo trecho
    lim = segs[idx+1]["a"] if idx+1 < len(segs) else NTOT
    while escrito < lim:
        f = proc.pop(escrito, None)
        if f is None: f = base_q(escrito)
        ff.stdin.write(f.tobytes()); buf.pop(escrito, None); escrito += 1
while escrito < NTOT:
    f = proc.pop(escrito, None)
    if f is None: f = base_q(escrito)
    ff.stdin.write(f.tobytes()); buf.pop(escrito, None); escrito += 1
ff.stdin.close(); ff.wait(); print("ok", escrito)

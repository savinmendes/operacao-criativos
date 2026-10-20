# -*- coding: utf-8 -*-
"""Correcao de cor (REVISAO-LOTE-C) do AD 06: refaz base_sem_legenda + base_lipsync NUMA GERACAO SO, a partir do ORIGINAL
(UNICOS_HD/06.mp4), dos PNGs do LaMa ja calculados (_tmp/lama, _tmp/mask; inclui o clarao 205-212 do lama_flash.py) e das
saidas do HeyGen ja baixadas (lipsync/out/ls_<n>.mp4), com a leitura/gravacao exata do ad13/lipsync3/comum3.py
(ffmpeg bt601 + accurate_rnd; conversao inversa exata; etiqueta bt709/tv so no bitstream). Nenhum LaMa novo, nenhum job novo.
- Base = _tmp/montar_base.py (faixa y 740-1090: LaMa colado so na mascara, borda suave, EMA 0,65/0,35 zerada nos cortes),
  com o PNG do LaMa reajustado por quadro (afim por canal LaMa -> original, medida na faixa FORA da mascara dilatada).
- Montagem = lipsync/recolocar.py (mesma elipse do nariz ao queixo seguindo a boca por MediaPipe na saida do HeyGen, mesma
  suavizacao, mesmos trechos, w6 com as caixas de boxes_w6.json, w4/w11 cobertos pelo plano.json, crossfade linear w5/w6).
- Cada trecho do HeyGen leva antes de colar o desvio de cor (BGR) medido num anel de pele em volta da elipse (fora dela)
  + um ajuste interno (mediana no miolo da elipse) aplicado com o peso da elipse (como no AD 08/12).
Uso (em ad06/lipsync): python recolocar_cor.py  -> ../base_sem_legenda.mp4 e ../base_lipsync.mp4 (2465 q, 24 fps)"""
import sys, os, json, subprocess
os.environ.setdefault("GLOG_minloglevel", "2")
import numpy as np, cv2
from pathlib import Path
AQ = Path(__file__).resolve().parent; AD = AQ.parent; T = AD.parent; P = T.parents[1]
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
ORIG = P / "UNICOS_HD" / "06.mp4"
cfg = json.loads((AQ / "segs.json").read_text()); FPS = cfg["fps"]; NTOT = cfg["ntot"]
plano = json.loads((AQ / "plano.json").read_text())
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=1,
    min_face_detection_confidence=0.3))
log = []
# ---------------- base nova (= _tmp/montar_base.py) ----------------
R0, R1 = 740, 1090
CORTES = set(range(200, 214)) | {209, 442, 677, 909, 958, 1298, 1474, 1714, 1831, 1905, 1987, 2072, 2190, 2319, 2381, 2413}
def base_gen():
    ema = None; fits = []
    for i, f in enumerate(quadros(ORIG, 0, NTOT)):
        if i in CORTES: ema = None
        m = np.load(AD / "_tmp" / "mask" / f"{i:04d}.npy").astype(np.float32)
        if m.sum() > 0:
            l = cv2.imread(str(AD / "_tmp" / "lama" / f"{i:04d}.png")).astype(np.float32)
            o = f[R0:R1].astype(np.float32)
            fora = cv2.dilate((m > 0).astype(np.uint8), np.ones((41, 41), np.uint8)) == 0; fora[::2] = False; fora[:, ::2] = False
            if fora.sum() > 2000:
                A = np.zeros((3, 2), np.float32)
                for c in range(3): A[c] = np.polyfit(l[..., c][fora], o[..., c][fora], 1)
                l = l * A[:, 0] + A[:, 1]; fits.append(A)
            ema = l if ema is None else 0.65 * l + 0.35 * ema
            al = np.maximum(cv2.GaussianBlur(m, (11, 11), 0), m)[..., None]
            f[R0:R1] = np.clip(ema * al + o * (1 - al), 0, 255).astype(np.uint8)
        else: ema = None
        yield f
    F = np.array(fits); log.append(f"LaMa -> original: ganho BGR {F[:, :, 0].mean(0).round(3)}, offset {F[:, :, 1].mean(0).round(2)} ({len(F)} quadros)")
# ---------------- colagem (= recolocar.py) + cor ----------------
def ler_cv2(p):
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
def colar_seg(s, bases, outs, outs_det):
    if "track" in s: BX = json.load(open(AQ / f"boxes_{s['n']}.json"))
    else: BX = [s["crop"]] * len(bases)
    n = len(bases); PAR = [None] * n; SIG = [None] * n; PTS = [None] * n; par = None
    for k, ((x, y, w, h), g) in enumerate(zip(BX, outs_det)):
        sx, sy = w/720, h/1280
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB))))
        if r.face_landmarks:
            p = np.array([(q.x*720*sx + x, q.y*1280*sy + y) for q in r.face_landmarks[0]])
            fw = p[454,0]-p[234,0]; nose = p[1]; chin = p[152]; mo = (p[13]+p[14])/2
            novo = np.array([mo[0], (nose[1]+chin[1])/2 + 0.05*(chin[1]-nose[1]), 0.40*abs(fw), 0.70*(chin[1]-nose[1])])
            par = novo if par is None else 0.6*novo + 0.4*par
            PTS[k] = ((p[2] + p[0]) / 2, p[199], abs(fw))
        if par is not None: PAR[k] = par.copy(); SIG[k] = max(4, 0.07*abs(par[2])*2.5)
    if par is None: return bases, None
    primeiro = next(i for i, v in enumerate(PAR) if v is not None)
    for i in range(primeiro): PAR[i] = par.copy(); SIG[i] = 6   # = recolocar.py: 1os quadros sem rosto usam a ultima elipse
    def M_(k): pr = PAR[k]; return elipse(pr[0], pr[1], max(pr[2], 20), max(pr[3], 20), SIG[k])
    # desvio no anel de pele em volta da elipse (fora dela), mediana de 12 quadros
    ks = np.linspace(0, n - 1, 12).astype(int); d0s = []
    for k in ks:
        x, y, w, h = BX[k]; M = M_(k)[..., 0]; dentro = M > 0.01; fw = PAR[k][2] / 0.40
        anel = cv2.dilate(dentro.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(0.5 * fw) | 1,) * 2)).astype(bool) & ~dentro
        cx = np.zeros_like(anel); cx[int(y) + 3:int(y + h) - 3, int(x) + 3:int(x + w) - 3] = True; anel &= cx
        if anel.sum() < 50: continue
        full = por(outs[k], x, y, w, h).astype(np.float32)
        d0s.append((bases[k].astype(np.float32) - full)[anel].mean(0))
    d0 = np.median(np.array(d0s), 0) if d0s else np.zeros(3, np.float32)
    # ajuste interno: MEDIANA de (base - saida corrigida) no miolo da elipse (peso > 0,5), por canal; a mediana ignora o
    # +/- do labio que mudou de lugar (no v1/w17 os 2 pontos fixos do AD 08 caiam na sombra do labio PT e escureciam a boca)
    dis = []
    for k in ks:
        x, y, w, h = BX[k]; M = M_(k)[..., 0] > 0.5
        if M.sum() < 50: continue
        full = por(outs[k], x, y, w, h).astype(np.float32) + d0
        dis.append(np.median((bases[k].astype(np.float32) - full)[M], 0))
    d1 = np.clip(np.median(np.array(dis), 0), -8, 8) if dis else np.zeros(3, np.float32)
    res = []
    for k in range(n):
        x, y, w, h = BX[k]; M = M_(k)
        full = por(outs[k], x, y, w, h).astype(np.float32) + d0 + d1 * M
        res.append(np.clip(full * M + bases[k] * (1 - M), 0, 255).astype(np.uint8))
    return res, (d0, d1)
def cobrir(bases, r):
    x, y, w, h = r[:4]
    if len(r) > 4: bases = [CACHE[r[4] + j] for j in range(len(bases))]
    return [cv2.resize(b[y:y+h, x:x+w], (720, 1280), interpolation=cv2.INTER_LANCZOS4) for b in bases]
# cache p/ a cobertura do w11 (quadros da mesma cena antes das setas)
CACHE_Q = set()
for s in cfg["segs"]:
    r = plano.get("cobrir", {}).get(s["n"])
    if r and len(r) > 4: CACHE_Q |= set(range(r[4], r[4] + s["b"] - s["a"]))
CACHE = {}
def enc(path, crf):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        *ENC_VF,"-threads","4","-c:v","libx264","-crf",str(crf),"-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(path)], stdin=subprocess.PIPE)
eb, el = enc(AD / "base_sem_legenda.mp4", 12), enc(AD / "base_lipsync.mp4", 14)
gen = base_gen(); buf = {}; lido = 0
def base_q(k):
    global lido
    while lido <= k:
        f = next(gen); eb.stdin.write(f.tobytes()); buf[lido] = f
        if lido in CACHE_Q: CACHE[lido] = f
        lido += 1
    return buf[k]
segs = sorted(cfg["segs"], key=lambda s: s["a"]); proc = {}; escrito = 0
for idx, s in enumerate(segs):
    a, b, n = s["a"], s["b"], s["b"] - s["a"]
    bases = [base_q(k) for k in range(a, b)]
    if s["n"] in plano.get("cobrir", {}):
        fr = cobrir(bases, plano["cobrir"][s["n"]]); tipo = "coberto"
    else:
        arq = AQ / plano.get(s["n"], f"out/ls_{s['n']}.mp4")
        od = ler_cv2(arq); oq = list(quadros(arq)); m_total = len(oq)
        assert len(od) == len(oq), (s["n"], len(od), len(oq))
        od = od[:n] if len(od) >= n else reamostrar(od, n); oq = oq[:n] if len(oq) >= n else reamostrar(oq, n)
        fr, dv = colar_seg(s, bases, oq, od)
        tipo = f"lipsync {arq.name} {m_total}q->{n}; desvio anel {dv[0].round(2)} + interno {dv[1].round(2)}"
    for j, k in enumerate(range(a, b)):
        if k in proc:   # sobreposicao: crossfade linear (= recolocar.py)
            ov = [q for q in range(a, b) if q in proc]; t = (ov.index(k)+1)/(len(ov)+1)
            proc[k] = np.clip(proc[k].astype(np.float32)*(1-t) + fr[j].astype(np.float32)*t, 0, 255).astype(np.uint8)
        else: proc[k] = fr[j]
    log.append(f"{s['n']} q{a}-{b-1}: {tipo}"); print(log[-1], flush=True)
    lim = segs[idx+1]["a"] if idx+1 < len(segs) else NTOT
    while escrito < lim:
        f = proc.pop(escrito, None)
        if f is None: f = base_q(escrito)
        el.stdin.write(f.tobytes()); buf.pop(escrito, None); escrito += 1
while escrito < NTOT:
    f = proc.pop(escrito, None)
    if f is None: f = base_q(escrito)
    el.stdin.write(f.tobytes()); buf.pop(escrito, None); escrito += 1
el.stdin.close(); el.wait()
while lido < NTOT: base_q(lido); buf.clear()
eb.stdin.close(); eb.wait()
try: next(gen)
except StopIteration: pass
print("\n".join(log)); print("ok", escrito, "quadros lipsync,", lido, "base")
(AQ / "recolocar_cor.log").write_text("\n".join(log), encoding="utf-8")

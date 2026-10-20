# -*- coding: utf-8 -*-
"""Lipsync com recorte RASTREADO no rosto de quem fala (tamanho e posição por quadro), para planos com câmera andando/zoom
ou com outro rosto que confunde o detector. Generaliza o ad08/lipsync/preparar.py + colar.py.

  python rastreado.py prep  cfg.json [nome ...]   -> lipsync/in/pt_<nome>.mp4 (recorte 720x1280 + ÁUDIO PT original),
                                                     lipsync/in/es_<nome>.mp3, lipsync/trilhas/<nome>.json
  python rastreado.py aplicar cfg.json            -> regrava cfg["saida"] (base_lipsync) a partir de cfg["inicio"]
                                                     (base_lipsync anterior), trocando só os quadros dos trechos refeitos

cfg: {"base": base limpa, "orig": original com o PT, "narr": narracao_es.wav, "inicio": base_lipsync antiga,
      "saida": base_lipsync nova, "dir": "lipsync",
      "trechos": [{"nome", "q0", "q1" (inclusivo), "fator": 2.4, "minw": 320, "pad": quadros p/ chegar a 90}]}
Rosto de quem fala: no 1º quadro, o de queixo mais baixo; depois, o mais perto do anterior. Detecção que pula longe
(> 0,5 largura do rosto) = descartada e interpolada (era o que fazia o recorte saltar no AD 08). Outros rostos dentro
do recorte = inpaint. Colagem: elipse suave na boca e queixo, saída reamostrada p/ o nº exato de quadros (sem congelar),
crossfade de 2 quadros nas emendas sem corte de câmera."""
import sys, os, json, subprocess
os.environ["GLOG_minloglevel"] = "2"
import cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
FPS = 30
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
_det = None
def rostos(f, roi=None):
    """roi = [x, y, w, h]: detecta num recorte ampliado 2x (rostos pequenos no plano aberto) e devolve em coordenadas do quadro"""
    if roi:
        x, y, w, h = roi; sub = cv2.resize(np.ascontiguousarray(f[y:y+h, x:x+w]), (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
        return [np.array([b[0] / 2 + x, b[1] / 2 + y, b[2] / 2 + x, b[3] / 2 + y]) for b in _det_px(sub)]
    return _det_px(f)
def _det_px(f):
    global _det
    if _det is None:
        _det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(
            model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
    r = _det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    return [np.array([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]) for p in
            [np.array([(q.x * f.shape[1], q.y * f.shape[0]) for q in fl]) for fl in r.face_landmarks]]
def suav(x, k=9):
    if len(x) < 3: return x
    k = min(k, len(x) // 2 * 2 - 1); p = k // 2
    return np.convolve(np.pad(x, (p, p), mode="edge"), np.ones(k) / k, mode="valid")
def ler(p, a=0, n=None):
    cap = cv2.VideoCapture(str(p)); cap.set(cv2.CAP_PROP_POS_FRAMES, a); fr = []
    while n is None or len(fr) < n:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    return fr
def enc(path):
    return subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-threads","4","-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p",*COR,"-an",str(path)], stdin=subprocess.PIPE)
def trilha(frames, fator, minw, semente=None, roi=None):
    n = len(frames); W = [None] * n; O = [[] for _ in range(n)]; prev = None
    if semente: prev = np.array([semente[0] - 1, semente[1] - 1, semente[0] + 1, semente[1] + 1], float)   # rosto inicial = o mais perto da semente
    for i, f in enumerate(frames):
        bx = rostos(f, roi)
        if not bx: continue
        if prev is None: w = max(bx, key=lambda t: t[1] + t[3])
        else:
            w = min(bx, key=lambda t: np.hypot((t[0]+t[2]-prev[0]-prev[2])/2, (t[1]+t[3]-prev[1]-prev[3])/2))
            fw = max(prev[2] - prev[0], 120)
            if np.hypot((w[0]+w[2]-prev[0]-prev[2])/2, (w[1]+w[3]-prev[1]-prev[3])/2) > 0.5 * fw: w = None
        O[i] = [t for t in bx if w is None or t is not w]
        if w is not None: W[i] = w; prev = w
    ok = [i for i in range(n) if W[i] is not None]
    Wa = np.array([np.interp(range(n), ok, [W[i][j] for i in ok]) for j in range(4)]).T
    fw = suav(Wa[:, 2] - Wa[:, 0], 15); cx = suav((Wa[:, 0] + Wa[:, 2]) / 2); cy = suav((Wa[:, 1] + Wa[:, 3]) / 2 + 0.15 * (Wa[:, 3] - Wa[:, 1]))
    if np.ptp(fw) < 0.08 * fw.mean() and cx.std() < 8 and cy.std() < 8:   # câmera parada: recorte fixo
        fw[:] = fw.max(); cx[:] = cx.mean(); cy[:] = cy.mean()
    Wc = np.clip(np.round(fator * fw / 2) * 2, minw, 720).astype(int); Hc = np.minimum(np.round(Wc * 16 / 9 / 2) * 2, 1280).astype(int)
    Wc = np.where(Hc == 1280, 720, Wc)
    X0 = np.clip(np.round(cx - Wc / 2), 0, 720 - Wc).astype(int); Y0 = np.clip(np.round(cy - Hc / 2), 0, 1280 - Hc).astype(int)
    return dict(X0=X0.tolist(), Y0=Y0.tolist(), W=Wc.tolist(), H=Hc.tolist(), rosto=Wa.round(1).tolist(), outros=[[o.round(1).tolist() for o in oo] for oo in O],
                det=len(ok) / n)
def prep(cfg, so):
    D = Path(cfg["dir"]); (D / "in").mkdir(parents=True, exist_ok=True); (D / "trilhas").mkdir(exist_ok=True)
    for t in cfg["trechos"]:
        if so and t["nome"] not in so: continue
        a, b = t["q0"], t["q1"]; n = b - a + 1; npad = t.get("pad", max(0, 90 - n))
        frames = ler(cfg["base"], a, n); T = trilha(frames, t.get("fator", 2.4), t.get("minw", 320), t.get("semente"), t.get("roi"))
        tmp = D / "in" / f"_v_{t['nome']}.mp4"; ff = enc(tmp); ninp = 0
        for i, f in enumerate(frames):
            x0, y0, w, h = T["X0"][i], T["Y0"][i], T["W"][i], T["H"][i]
            c = np.ascontiguousarray(f[y0:y0+h, x0:x0+w]); m = np.zeros(c.shape[:2], np.uint8)
            for o in T["outros"][i]:
                ex, ey = 0.15 * (o[2] - o[0]), 0.15 * (o[3] - o[1])
                cv2.rectangle(m, (int(o[0]-ex-x0), int(o[1]-ey-y0)), (int(o[2]+ex-x0), int(o[3]+ey-y0)), 255, -1)
            r = T["rosto"][i]; ex, ey = 0.1 * (r[2] - r[0]), 0.1 * (r[3] - r[1])
            cv2.rectangle(m, (int(r[0]-ex-x0), int(r[1]-ey-y0)), (int(r[2]+ex-x0), int(r[3]+ey-y0)), 0, -1)
            if m.any(): c = cv2.inpaint(c, m, 5, cv2.INPAINT_TELEA); ninp += 1
            last = cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4); ff.stdin.write(last.tobytes())
        for _ in range(npad): ff.stdin.write(last.tobytes())
        ff.stdin.close(); ff.wait()
        t0 = a / FPS; dur = (n + npad) / FPS; t1 = (b + 1) / FPS
        subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",cfg["orig"],"-filter_complex",
            f"[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,apad=whole_dur={dur}[a]","-map","0:v","-map","[a]",
            "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dur}",str(D / "in" / f"pt_{t['nome']}.mp4")], check=True); tmp.unlink()
        subprocess.run(["ffmpeg","-v","error","-y","-i",cfg["narr"],"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS,apad=whole_dur={dur}",
            "-ac","1","-c:a","libmp3lame","-b:a","192k",str(D / "in" / f"es_{t['nome']}.mp3")], check=True)
        T.pop("outros"); json.dump(T, open(D / "trilhas" / f"{t['nome']}.json", "w"))
        print(t["nome"], a, b, n, "pad", npad, "recorte W", min(T["W"]), "-", max(T["W"]), "det", f"{T['det']:.0%}", "inpaint q", ninp, flush=True)
def reamostrar(fr, n):
    m = len(fr)
    if m == n: return fr
    out = []
    for i in range(n):
        x = i * (m - 1) / max(1, n - 1); j = int(np.floor(x)); a = x - j
        out.append(fr[-1] if j >= m - 1 else (fr[j] if a < 1e-3 else cv2.addWeighted(fr[j], 1 - a, fr[j + 1], a, 0)))
    return out
def colar_q(base, g, T, i):
    x0, y0, w, h = T["X0"][i], T["Y0"][i], T["W"][i], T["H"][i]; r = T["rosto"][i]
    full = base.copy(); full[y0:y0+h, x0:x0+w] = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA)
    fw, fh = r[2] - r[0], r[3] - r[1]; m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int((r[0]+r[2])/2), int(r[1] + 0.68*fh)), (int(0.42*fw + 6), int(0.36*fh + 8)), 0, 0, 360, 1.0, -1)
    m[:y0, :] = 0; m[y0+h:, :] = 0; m[:, :x0] = 0; m[:, x0+w:] = 0
    m = cv2.GaussianBlur(m, (0, 0), max(4, fw / 25))[..., None]
    return np.clip(full * m + base * (1 - m), 0, 255).astype(np.uint8), m
def aplicar(cfg):
    D = Path(cfg["dir"]); out = ler(cfg["inicio"]); base = ler(cfg["base"]); N = len(out); log = []
    for t in cfg["trechos"]:
        a, b = t["q0"], t["q1"]; n = b - a + 1; T = json.load(open(D / "trilhas" / f"{t['nome']}.json"))
        g = ler(D / "out" / f"ls_{t['nome']}.mp4"); m0 = len(g); g = reamostrar(g[:n] if len(g) > n else g, n)
        masks = []
        for k in range(n):
            if a + k < N: out[a + k], mk = colar_q(base[a + k], g[k], T, k); masks.append(mk)
        for q, mk, lado in ((a, masks[0], "ini"), (b + 1, masks[-1], "fim")):   # emendas com o vizinho antigo
            if q <= 0 or q >= N: continue
            corte = np.abs(base[q - 1].astype(np.float32) - base[q]).mean() > 10
            if corte: log.append(f"{t['nome']} {lado} q{q}: corte de câmera"); continue
            L, R = out[q - 1].astype(np.float32), out[q].astype(np.float32)
            M = mk
            out[q - 1] = np.clip((L * 2/3 + R / 3) * M + L * (1 - M), 0, 255).astype(np.uint8)
            out[q] = np.clip((L / 3 + R * 2/3) * M + R * (1 - M), 0, 255).astype(np.uint8)
            log.append(f"{t['nome']} {lado} q{q}: contínua, crossfade 2 q na boca")
        log.append(f"{t['nome']}: saída {m0} q -> {n}")
    e = enc(cfg["saida"])
    for f in out: e.stdin.write(f.tobytes())
    e.stdin.close(); e.wait(); print("\n".join(log)); print("ok", N)
if __name__ == "__main__":
    cfg = json.load(open(sys.argv[2], encoding="utf-8"))
    prep(cfg, set(sys.argv[3:])) if sys.argv[1] == "prep" else aplicar(cfg)

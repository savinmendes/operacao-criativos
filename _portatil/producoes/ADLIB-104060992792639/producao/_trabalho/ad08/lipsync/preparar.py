# -*- coding: utf-8 -*-
"""AD 08: entrada do HeyGen recortada no rosto da Desatadora, com rastreamento por quadro (a câmera anda em s07/s08).
- rosto da mulher: o de queixo mais baixo no 1º quadro, depois o mais perto do anterior; quadros sem detecção = interpolados;
- recorte 9:16 de largura ~2x o rosto (mín. 270), centro suavizado (fixo se a câmera é parada);
- outros rostos (Jesus) dentro do recorte = inpaint (fora do rosto dela);
- escala p/ 720x1280, 30 fps, ÁUDIO ORIGINAL PT; ES separado; < 3 s completado com o último quadro.
Salva trilhas/sNN.json (recorte e caixa do rosto por quadro), usadas pelo colar.py. Uso: python preparar.py [sNN ...]"""
import sys, os, json, subprocess; os.environ["GLOG_minloglevel"] = "2"
import cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from segs import SEGS, FPS
AQ = Path(__file__).parent; AD = AQ.parent; SRC = AD.parent.parent.parent / "UNICOS_HD/08.mp4"
(AQ / "in").mkdir(exist_ok=True); (AQ / "trilhas").mkdir(exist_ok=True)
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))
def rostos(f):
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))))
    return [np.array([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()]) for p in
            [np.array([(q.x * 720, q.y * 1280) for q in fl]) for fl in r.face_landmarks]]
def suav(x, k=15):
    if len(x) < 3: return x
    k = min(k, len(x) // 2 * 2 - 1); pad = k // 2
    xp = np.pad(x, (pad, pad), mode="edge"); return np.convolve(xp, np.ones(k) / k, mode="valid")
def gerar(k):
    a, b = SEGS[k - 1]; nome = f"s{k:02d}"; n = b - a + 1
    cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
    frames = [cap.read()[1] for _ in range(n)]
    W = [None] * n; O = [[] for _ in range(n)]; prev = None
    for i, f in enumerate(frames):
        bx = rostos(f)
        if not bx: continue
        w = max(bx, key=lambda t: t[1] + t[3])   # mulher = rosto mais baixo (centro y): Jesus fica atrás e mais alto
        W[i] = w; O[i] = [t for t in bx if t is not w]
    det_o = [i for i in range(n) if O[i]]
    for i in range(n):   # quadros sem o outro rosto detectado: usa o do quadro mais próximo (até 15 q)
        if not O[i] and det_o:
            j = min(det_o, key=lambda j: abs(j - i))
            if abs(j - i) <= 15: O[i] = O[j]
    ok = [i for i in range(n) if W[i] is not None]
    Wa = np.array([np.interp(range(n), ok, [W[i][j] for i in ok]) for j in range(4)]).T
    fw = (Wa[:, 2] - Wa[:, 0]); cx = (Wa[:, 0] + Wa[:, 2]) / 2; cy = (Wa[:, 1] + Wa[:, 3]) / 2 + 0.15 * (Wa[:, 3] - Wa[:, 1])
    Wc = int(np.clip(round(2.0 * fw.max() / 2) * 2, 270, 720)); Hc = int(round(Wc * 16 / 9 / 2) * 2)
    if Hc > 1280: Hc = 1280; Wc = 720
    if cx.std() < 8 and cy.std() < 8: cxs = np.full(n, cx.mean()); cys = np.full(n, cy.mean())
    else: cxs, cys = suav(cx), suav(cy)
    X0 = np.clip(np.round(cxs - Wc / 2), 0, 720 - Wc).astype(int); Y0 = np.clip(np.round(cys - Hc / 2), 0, 1280 - Hc).astype(int)
    npad = max(0, 90 - n)
    tmp = AQ / "in" / f"_v_{nome}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-threads","4","-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p","-color_range","tv","-colorspace","bt709",
        "-color_primaries","bt709","-color_trc","bt709",str(tmp)], stdin=subprocess.PIPE)
    ninp = 0
    for i, f in enumerate(frames):
        x0, y0 = X0[i], Y0[i]; c = np.ascontiguousarray(f[y0:y0+Hc, x0:x0+Wc])
        m = np.zeros(c.shape[:2], np.uint8)
        for o in O[i]:
            ex, ey = 0.15 * (o[2] - o[0]), 0.15 * (o[3] - o[1])
            cv2.rectangle(m, (int(o[0]-ex-x0), int(o[1]-ey-y0)), (int(o[2]+ex-x0), int(o[3]+ey-y0)), 255, -1)
        w = Wa[i]; ex, ey = 0.1 * (w[2] - w[0]), 0.1 * (w[3] - w[1])
        cv2.rectangle(m, (int(w[0]-ex-x0), int(w[1]-ey-y0)), (int(w[2]+ex-x0), int(w[3]+ey-y0)), 0, -1)
        if m.any(): c = cv2.inpaint(c, m, 5, cv2.INPAINT_TELEA); ninp += 1
        last = cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4); ff.stdin.write(last.tobytes())
    for _ in range(npad): ff.stdin.write(last.tobytes())
    ff.stdin.close(); ff.wait()
    t0 = a / FPS; dur = (n + npad) / FPS; t1r = (b + 1) / FPS
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(SRC),"-filter_complex",
        f"[1:a]atrim={t0}:{t1r},asetpts=PTS-STARTPTS,apad=whole_dur={dur}[a]","-map","0:v","-map","[a]",
        "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dur}",str(AQ / "in" / f"pt_{nome}.mp4")], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",
        f"atrim={t0}:{t1r},asetpts=PTS-STARTPTS,apad=whole_dur={dur}","-ac","1","-c:a","libmp3lame","-b:a","192k",
        str(AQ / "in" / f"es_{nome}.mp3")], check=True)
    json.dump({"X0": X0.tolist(), "Y0": Y0.tolist(), "W": Wc, "H": Hc, "rosto": Wa.round(1).tolist()}, open(AQ / "trilhas" / f"{nome}.json", "w"))
    print(nome, a, b, n, "pad", npad, "recorte", Wc, Hc, "fixo" if cx.std() < 8 and cy.std() < 8 else "movel", "det", f"{len(ok)/n:.0%}", "inpaint q", ninp, flush=True)
    return {"nome": nome, "quadro_ini": a, "quadro_fim": b, "n": n, "pad": npad}
so = sys.argv[1:]; segs = []
for k in range(2, len(SEGS) + 1):
    if so and f"s{k:02d}" not in so: continue
    segs.append(gerar(k))
if not so: json.dump({"fps": FPS, "cobrir": {"s01": {"quadros": [0, 285], "recorte": [110, 560, 380, 676]}}, "segmentos": segs}, open(AD / "segmentos.json", "w"), indent=1)

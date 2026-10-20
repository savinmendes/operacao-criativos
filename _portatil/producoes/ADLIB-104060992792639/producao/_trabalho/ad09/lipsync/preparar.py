# -*- coding: utf-8 -*-
"""Prepara a entrada do HeyGen recortada SÓ no rosto de quem fala (rastreado quadro a quadro), com os outros rostos
apagados (inpaint) dentro do recorte. Vídeo de entrada leva o ÁUDIO ORIGINAL PT; o ES vai separado.
Uso: python preparar.py NN segs.json [nomes...]
segs.json: {"fps":24, "base":"../base_sem_legenda.mp4", "segs":[{"nome":"A","q":[212,444],"regra":"baixo","larg":2.0}, ...]}
Saída: in/crop_<nome>.mp4 (720x1280, 24 fps, áudio PT), in/es_<nome>.mp3, in/pt_<nome>.wav, boxes/<nome>.json (caixas por quadro)."""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AQ = Path(__file__).parent; AD = AQ.parent
(AQ / "in").mkdir(exist_ok=True); (AQ / "boxes").mkdir(exist_ok=True)
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=4,
    min_face_detection_confidence=0.2, min_face_presence_confidence=0.2))
NN = sys.argv[1]; CFG = json.load(open(AQ / sys.argv[2], encoding="utf-8")); FPS = CFG["fps"]
so = set(sys.argv[3:])
ORIG = AD.parent.parent.parent / "UNICOS_HD" / f"{NN}.mp4"
KEY = {"baixo": lambda p: p[13][1], "esq": lambda p: -p[:, 0].mean(), "dir": lambda p: p[:, 0].mean(), "maior": lambda p: np.ptp(p[:, 0])}
def bbox(p): return np.array([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()])
def suav(a, w=9):
    a = np.asarray(a, float); out = a.copy(); h = w // 2
    for i in range(len(a)): out[i] = np.median(a[max(0, i-h):i+h+1], 0)
    k = np.ones(5) / 5; pad = np.pad(out, ((2, 2), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, j], k, "valid") for j in range(a.shape[1])], 1)

for sg in CFG["segs"]:
    nome = sg["nome"]
    if so and nome not in so: continue
    a, b = sg["q"]; n = b - a + 1
    capo = cv2.VideoCapture(str(ORIG)); capo.set(cv2.CAP_PROP_POS_FRAMES, a)
    capb = cv2.VideoCapture(str(AD / CFG["base"])); capb.set(cv2.CAP_PROP_POS_FRAMES, a)
    F, FA, BX, OT, LM = [], [], [], [], []
    last = None
    for k in range(n):
        ok, fo = capo.read(); ok2, fb = capb.read(); assert ok and ok2
        F.append(fb)
        bx0, by0, bx1, by1 = sg.get("busca", [0, 0, 720, 1280]); esc = sg.get("esc", 2.0 if "busca" in sg else 1.0)
        cb = cv2.resize(fo[by0:by1, bx0:bx1], None, fx=esc, fy=esc, interpolation=cv2.INTER_CUBIC)
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(cv2.cvtColor(cb, cv2.COLOR_BGR2RGB))))
        ps = [np.array([(bx0 + q.x * cb.shape[1] / esc, by0 + q.y * cb.shape[0] / esc) for q in fl]) for fl in r.face_landmarks]
        todos = list(ps)
        if "roi" in sg:   # só rostos com o centro dentro da roi
            x0, y0, x1, y1 = sg["roi"]; ps = [p for p in ps if x0 <= p[:, 0].mean() <= x1 and y0 <= p[:, 1].mean() <= y1]
        if ps:
            ps.sort(key=KEY[sg["regra"]]); s = ps[-1]; bs = bbox(s)
            if last is not None and np.abs(bs - last).max() > 80 and len(ps) > 1:   # troca de rosto: fica com o mais perto
                ps.sort(key=lambda p: np.abs(bbox(p) - last).sum()); s = ps[0]; bs = bbox(s)
            last = bs
            BX.append(bs); LM.append([s[13][0], s[13][1], s[14][0], s[14][1]])
            OT.append([bbox(p).tolist() for p in todos if p is not s and
                       (min(bs[2], bbox(p)[2]) - max(bs[0], bbox(p)[0])) * (min(bs[3], bbox(p)[3]) - max(bs[1], bbox(p)[1])) < 0.5 * np.prod(bbox(p)[2:] - bbox(p)[:2])])
        else:
            BX.append(None); LM.append(None); OT.append([])
    idx = [i for i in range(n) if BX[i] is not None]
    assert idx, f"{nome}: nenhum rosto"
    for i in range(n):   # preenche faltas com o vizinho
        if BX[i] is None:
            j = min(idx, key=lambda j: abs(j - i)); BX[i] = BX[j]; LM[i] = LM[j]
    B = suav(np.array(BX))
    cx = (B[:, 0] + B[:, 2]) / 2; fw = B[:, 2] - B[:, 0]; fh = B[:, 3] - B[:, 1]; cy = B[:, 1] + 0.55 * fh
    W = sg.get("larg", 2.0) * fw; H = W * 16 / 9
    crop = np.stack([cx - W / 2, cy - H * 0.45, W, H], 1)
    boxes = []
    tmp = AQ / "in" / f"_v_{nome}.mp4"
    COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p",*COR,str(tmp)], stdin=subprocess.PIPE)
    big = 400
    for i in range(n):
        x, y, w, h = crop[i]
        f = cv2.copyMakeBorder(F[i], big, big, big, big, cv2.BORDER_REPLICATE)
        m = np.zeros(f.shape[:2], np.uint8)
        for o in OT[i]:
            ox0, oy0, ox1, oy1 = [int(round(v)) for v in o]; mx = int(0.15 * (ox1 - ox0))
            m[oy0 + big - mx: oy1 + big + mx, ox0 + big - mx: ox1 + big + mx] = 255
        X0, Y0 = int(round(x)) + big, int(round(y)) + big; Wi, Hi = int(round(w)), int(round(h))
        c = np.ascontiguousarray(f[Y0:Y0 + Hi, X0:X0 + Wi]); mc = m[Y0:Y0 + Hi, X0:X0 + Wi]
        # não apaga o rosto de quem fala
        bs = B[i]; sx0, sy0, sx1, sy1 = int(bs[0]) + big - X0, int(bs[1]) + big - Y0, int(bs[2]) + big - X0, int(bs[3]) + big - Y0
        mc[max(0, sy0):max(0, sy1), max(0, sx0):max(0, sx1)] = 0
        if mc.any(): c = cv2.inpaint(c, mc, 7, cv2.INPAINT_TELEA)
        ff.stdin.write(cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4).tobytes())
        boxes.append(dict(crop=[X0 - big, Y0 - big, Wi, Hi], face=B[i].round(1).tolist()))
    pad = max(0, int(round(sg.get("min_s", 3.0) * FPS)) - n)
    for _ in range(pad): ff.stdin.write(cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4).tobytes())
    ff.stdin.close(); ff.wait()
    t0, dur = a / FPS, n / FPS; tot = (n + pad) / FPS
    pt = AQ / "in" / f"pt_{nome}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"_audio"/"orig.wav"),"-af",f"atrim={t0}:{t0+dur},asetpts=PTS-STARTPTS,apad=whole_dur={tot}",
                    "-ac","1","-ar","48000",str(pt)], check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(pt),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k",
                    str(AQ/"in"/f"crop_{nome}.mp4")], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"narracao_es.wav"),"-af",f"atrim={t0}:{t0+dur},asetpts=PTS-STARTPTS,apad=whole_dur={tot}",
                    "-ac","1","-c:a","libmp3lame","-b:a","192k",str(AQ/"in"/f"es_{nome}.mp3")], check=True)
    json.dump(dict(q=[a, b], n=n, pad=pad, boxes=boxes), open(AQ/"boxes"/f"{nome}.json","w"))
    print(nome, n, "quadros, detectados", len(idx), "pad", pad, "crop médio", np.round(crop.mean(0)).tolist(), "outros/quadro", round(np.mean([len(o) for o in OT]), 2), flush=True)

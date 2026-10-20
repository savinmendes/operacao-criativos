# -*- coding: utf-8 -*-
"""Cola a saida do HeyGen de volta na cena (so boca/queixo, elipse suave seguindo o rosto por quadro),
com correcao de cor (afim BGR 3x4 robusta medida no anel em volta da elipse, como _lote/cor_trecho.py).
Leitura/gravacao com matriz bt601 fixa (comum3). Saidas: mont/cena_KK_ls.mp4, lipsync/chk/full_cKK.mp4 (+ES) e orig_cKK.mp4 (+PT).
Uso: python colar_ls.py [cKK ...]"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\_lote")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar
from cor_trecho import ajustar, aplicar
import checar_lipsync as cl
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
AQ = Path(__file__).resolve().parent; L = AQ / "lipsync"; M = AQ / "mont"; CHK = L / "chk"; CHK.mkdir(exist_ok=True)
JOBS = json.load(open(L / "jobs.json", encoding="utf-8"))
det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path=str(cl._modelo())), running_mode=vision.RunningMode.IMAGE, num_faces=3))


def enc(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                            *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-an", str(path)], stdin=subprocess.PIPE)


def rosto(f, regiao=None):
    """(cx, cy da boca, largura do rosto, altura do rosto) do maior rosto (dentro da regiao, se dada)"""
    x0, y0, w, h = regiao or (0, 0, 720, 1280)
    sub = np.ascontiguousarray(cv2.cvtColor(f[y0:y0 + h, x0:x0 + w], cv2.COLOR_BGR2RGB))
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=sub)); best = None
    for fl in r.face_landmarks:
        p = np.array([(a.x * w + x0, a.y * h + y0) for a in fl])
        fw = np.linalg.norm(p[234] - p[454]); fh = np.linalg.norm(p[10] - p[152])
        if best is None or fw > best[2]: best = ((p[13, 0] + p[14, 0]) / 2, (p[13, 1] + p[14, 1]) / 2, fw, fh)
    return best


def suaviza(v):
    v = np.array(v, float); idx = np.arange(len(v)); ok = ~np.isnan(v[:, 0])
    if ok.sum() == 0: return None
    for j in range(v.shape[1]): v[:, j] = np.interp(idx, idx[ok], v[ok, j])
    k = 5; pad = np.pad(v, ((k // 2, k // 2), (0, 0)), mode="edge")
    return np.array([np.median(pad[i:i + k], 0) for i in range(len(v))])


def mascara(cx, cy, fw, fh, esc=1.0):
    m = np.zeros((1280, 720), np.float32)
    cv2.ellipse(m, (int(cx), int(cy + 0.06 * fh)), (int(0.36 * fw * esc), int(0.27 * fh * esc)), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, 0.06 * fw))


def processa(nome):
    J = JOBS[nome]; k = J["k"]; n = J["n"]
    base = list(quadros(M / f"cena_{k:02d}.mp4")); n = len(base)
    g = list(quadros(L / "out" / f"{nome}.mp4")); g = reamostrar(g, n) if len(g) != n else g
    if J["crop"]:
        x, y, w, h = J["crop"]; full = []
        for b, gg in zip(base, g):
            f = b.copy(); f[y:y + h, x:x + w] = cv2.resize(gg, (w, h), interpolation=cv2.INTER_AREA); full.append(f)
        g = full
    reg = tuple(J["crop"]) if J["crop"] else None
    R = []
    for b in base:
        r = rosto(b, reg); R.append(r if r else (np.nan,) * 4)
    R = suaviza(R)
    if R is None: print(nome, "SEM ROSTO"); return
    # cor: afim no anel (fora da elipse, dentro de 1,7x) em ~12 quadros
    X, Y = [], []
    for i in np.linspace(0, n - 1, min(12, n)).astype(int):
        m1 = mascara(*R[i]) > 0.02; m2 = mascara(*R[i], esc=1.7) > 0.5; anel = m2 & ~m1
        X.append(g[i][anel][::3]); Y.append(base[i][anel][::3])
    A, res, inl = ajustar(np.vstack(X), np.vstack(Y))
    out = enc(M / f"cena_{k:02d}_ls.mp4")
    for i in range(n):
        Mk = mascara(*R[i])[..., None]
        gc = aplicar(A, g[i]).reshape(g[i].shape)
        o = np.clip(gc * Mk + base[i].astype(np.float32) * (1 - Mk) + 0.5, 0, 255).astype(np.uint8)
        out.stdin.write(o.tobytes())
    out.stdin.close(); out.wait()
    # arquivos de conferencia
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(M / f"cena_{k:02d}_ls.mp4"), "-i", str(L / "in" / f"{nome}_es.mp3"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", str(CHK / f"full_{nome}.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(M / f"cena_{k:02d}.mp4"), "-i", str(L / "in" / f"{nome}_pt.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", str(CHK / f"orig_{nome}.mp4")], check=True)
    rr = R[n // 2]
    print(f"{nome}: {n} q, cor afim residuo {res:.2f} inliers {inl:.2f}, rosto ~({rr[0]:.0f},{rr[1]:.0f}) fw {rr[2]:.0f}", flush=True)
    return rr


if __name__ == "__main__":
    nomes = sys.argv[1:] or list(JOBS)
    info = {}
    for nm in nomes:
        rr = processa(nm)
        if rr is not None: info[nm] = [float(x) for x in rr]
    json.dump(info, open(L / "rostos.json", "w"), indent=0)

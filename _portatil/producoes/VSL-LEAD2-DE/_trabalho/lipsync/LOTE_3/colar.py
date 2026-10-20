# -*- coding: utf-8 -*-
"""Cola a boca e o queixo da saida do HeyGen (heygen/<id>.mp4) sobre o fundo base/<id>.mp4 (original esticado,
N quadros exatos) e grava <id>.mp4 (so video, bt601 fixo). Mede com checar_lipsync.py e grava chk/<id>.json.
Uso: python colar.py [id ...]"""
import json, subprocess, sys, os
from pathlib import Path
import numpy as np, cv2

W = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from comum3 import quadros, ENC_VF, ENC_TAG, reamostrar  # noqa: E402
import checar_lipsync as CL  # noqa: E402

KIT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py"
CROP_PULPITO = (200, 0, 360, 480)
PREP = json.load(open(W / "prep.json", encoding="utf-8"))
Wd, Hd = 720, 960


def landmarks(frames):
    """por quadro: (cx, cy, ax, ay) da elipse de boca+queixo; None se nao achou."""
    tr = CL.Rastreador()
    out = []
    for f in frames:
        p = tr.pontos(f)
        if p is None:
            out.append(None); continue
        fw = np.linalg.norm(p[234] - p[454])
        boca = p[[13, 14, 61, 291]].mean(0)
        nariz, queixo = p[2], p[152]
        cy = (nariz[1] + queixo[1]) / 2 + 0.05 * (queixo[1] - nariz[1])
        out.append((boca[0], cy, 0.42 * fw, 0.62 * (queixo[1] - nariz[1])))
    tr.close()
    # preenche falhas e suaviza (mediana movel de 5)
    idx = [i for i, v in enumerate(out) if v is not None]
    if not idx:
        return None
    A = np.array([out[i] for i in idx], float)
    full = np.stack([np.interp(range(len(out)), idx, A[:, k]) for k in range(4)], 1)
    sm = full.copy()
    for i in range(len(full)):
        sm[i] = np.median(full[max(0, i - 2):i + 3], 0)
    return sm, len(idx) / len(out)


def mascara(c):
    m = np.zeros((Hd, Wd), np.float32)
    cx, cy, ax, ay = c
    cv2.ellipse(m, (int(cx), int(cy)), (max(4, int(ax)), max(4, int(ay))), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, 0.18 * ax))


def processar(i):
    info = PREP[i]; n = info["n"]
    hg = W / "heygen" / f"{i}.mp4"
    base = list(quadros(W / "base" / f"{i}.mp4", 0, n, Wd, Hd))
    g = list(quadros(hg, 0, None, Wd, Hd))
    ng = len(g)
    g = reamostrar(g, n) if ng != n else g
    if info["pulpito"]:
        x, y, w, h = CROP_PULPITO
        M = np.float32([[w / Wd, 0, x], [0, h / Hd, y]])
        g = [cv2.warpAffine(f, M, (Wd, Hd), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE) for f in g]
    lm = landmarks(base)
    if lm is None:
        raise RuntimeError("sem rosto")
    C, cobertura = lm
    # cor: anel em volta da elipse (fora dela), mediana de ~12 quadros
    dif = []
    for k in np.linspace(0, n - 1, min(12, n)).astype(int):
        m = mascara(C[k]); anel = (cv2.GaussianBlur((m > 0.02).astype(np.float32), (0, 0), 10) > 0.05) & (m < 0.02)
        if anel.sum() > 50:
            dif.append(np.median(base[k][anel].astype(np.float32) - g[k][anel].astype(np.float32), 0))
    dv = np.clip(np.median(dif, 0) if dif else np.zeros(3), -10, 10)
    out = W / f"{i}.mp4"
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{Wd}x{Hd}", "-r", "30",
                           "-i", "-", *ENC_VF, "-threads", "4", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                           *ENC_TAG, "-an", str(out)], stdin=subprocess.PIPE)
    for k in range(n):
        m = mascara(C[k])[..., None]
        gk = np.clip(g[k].astype(np.float32) + dv, 0, 255)
        f = np.clip(gk * m + base[k].astype(np.float32) * (1 - m) + 0.5, 0, 255).astype(np.uint8)
        pr.stdin.write(f.tobytes())
    pr.stdin.close(); pr.wait()
    # aceite
    r = subprocess.run([sys.executable, KIT, str(out), "--audio-novo", str(W / "in" / f"a_{i}.mp3"),
                        "--original", str(W / "base" / f"{i}.mp4"), "--sem-audio-original"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    txt = r.stdout.strip()
    import re
    mm = re.search(r"ndice de pausa ([0-9.]+)", txt)
    idx = float(mm.group(1)) if mm and mm.group(1) not in ("-",) else None
    st = txt.splitlines()[-1].split(":")[0] if txt else "ERRO"
    res = {"id": i, "quadros_heygen": ng, "quadros": n, "cobertura_rosto": round(cobertura, 3),
           "desvio_cor_bgr": [round(float(x), 2) for x in dv], "indice_pausa": idx, "checar": st, "saida_checar": txt}
    (W / "chk").mkdir(exist_ok=True)
    json.dump(res, open(W / "chk" / f"{i}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(i, ng, n, f"cob {cobertura:.2f}", "cor", res["desvio_cor_bgr"], "pausa", idx, st, flush=True)


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(PREP)
    for i in ids:
        if not (W / "heygen" / f"{i}.mp4").exists():
            print(i, "sem saida heygen"); continue
        try:
            processar(i)
        except Exception as e:
            print(i, "ERRO", e, flush=True)

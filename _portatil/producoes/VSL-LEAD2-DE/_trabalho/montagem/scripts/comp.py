# -*- coding: utf-8 -*-
"""Para cada trecho de lipsync: alinha cada quadro do <id>.mp4 ao quadro certo da base_limpa_live (busca +-4 quadros),
acha boca/queixo (MediaPipe no quadro do lipsync), cola SO a elipse da boca sobre a base limpa, tirando as caixas de
legenda ES do OCR. Grava comp/<id>.mp4 (bt601 fixo, crf 12) + comp/<id>.json.  Uso: python comp.py id [id ...]"""
import sys, json, subprocess, os
import numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from vslcomum import *
import checar_lipsync as CL

LOT = {t["id"]: t for t in json.load(open(T / "voz" / "lotes.json", encoding="utf-8"))["trechos"]}
OCR = {int(k): v for k, v in json.load(open(T / "base" / "ocr_boxes.json", encoding="utf-8")).items()}
OUT = M / "comp"; OUT.mkdir(exist_ok=True)
ENC = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
       "-c:v", "libx264", "-preset", "fast", "-crf", "12",
       "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]


def caixas_ocr(j):
    b = []
    for q in range(6 * (j // 6) - 12, 6 * (j // 6) + 19, 6):
        b += OCR.get(q, [])
    return b


def landmarks(frames):
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
    idx = [i for i, v in enumerate(out) if v is not None]
    if not idx:
        return None, 0.0
    A = np.array([out[i] for i in idx], float)
    full = np.stack([np.interp(range(len(out)), idx, A[:, k]) for k in range(4)], 1)
    sm = full.copy()
    for i in range(len(full)):
        sm[i] = np.median(full[max(0, i - 2):i + 3], 0)
    return sm, len(idx) / len(out)


def elipse_por_diferenca(lip, bas):
    """fallback: regiao que mais muda (fora da faixa de legenda/selo) = boca"""
    acc = np.zeros((H, W), np.float32)
    for a, b in zip(lip[::5], bas[::5]):
        acc += np.abs(a.astype(np.float32) - b.astype(np.float32)).sum(2)
    acc[:80] = 0; acc[640:] = 0
    acc = cv2.GaussianBlur(acc, (0, 0), 6)
    y, x = np.unravel_index(np.argmax(acc), acc.shape)
    return (float(x), float(y), 28.0, 30.0)


def processar(tid):
    t = LOT[tid]; lote = t["lote"]
    src = T / "lipsync" / f"LOTE_{lote}" / f"{tid}.mp4"
    lip = ler(src)
    N = len(lip)
    q0 = int(round(t["novo_ini"] * FPS))
    js = [int(round(novo2orig((q0 + k) / FPS) * FPS)) for k in range(N)]
    a = max(0, min(js) - 5); b = max(js) + 5
    bas = ler(BASE, a / FPS, b - a + 1)
    def g(f): return cv2.resize(cv2.cvtColor(f[80:620], cv2.COLOR_BGR2GRAY), (180, 135)).astype(np.float32)
    gb = [g(f) for f in bas]
    ds = []
    for k in range(N):
        gl = g(lip[k]); best = None
        for d in range(-4, 5):
            i = js[k] + d - a
            if 0 <= i < len(gb):
                e = np.abs(gl - gb[i]).mean()
                if best is None or e < best[0]: best = (e, d)
        ds.append(best[1])
    ds = np.array(ds)
    dm = ds
    erro = []
    sel = [bas[js[k] + dm[k] - a] for k in range(N)]
    for k in range(0, N, 10):
        erro.append(float(np.abs(g(lip[k]) - g(sel[k])).mean()))
    lm, cob = landmarks(lip)
    fallback = lm is None
    if fallback:
        e = elipse_por_diferenca(lip, sel); lm = np.array([e] * N)
    # correcao de cor: fora da boca, regiao 80-620
    dv = []
    for k in range(0, N, max(1, N // 12)):
        m = np.ones((H, W), np.uint8); m[:80] = 0; m[620:] = 0
        cx, cy, ax, ay = lm[k]
        cv2.ellipse(m, (int(cx), int(cy)), (int(ax * 1.6), int(ay * 1.6)), 0, 0, 360, 0, -1)
        dv.append((sel[k].astype(np.float32) - lip[k].astype(np.float32))[m.astype(bool)].mean(0))
    dv = np.median(dv, 0)
    if np.abs(dv).max() > 6: dv = np.zeros(3, np.float32)
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                           "-i", "-"] + ENC + [str(OUT / f"{tid}.mp4")], stdin=subprocess.PIPE)
    for k in range(N):
        cx, cy, ax, ay = lm[k]
        m = np.zeros((H, W), np.float32)
        cv2.ellipse(m, (int(cx), int(cy)), (max(4, int(ax)), max(4, int(ay))), 0, 0, 360, 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), max(3, 0.18 * ax))
        for (x0, y0, x1, y1) in caixas_ocr(js[k] + dm[k]):
            m[max(0, y0 - 8):y1 + 8, max(0, x0 - 8):x1 + 8] = 0
        m[:80] = 0  # selo
        m = m[..., None]
        l = np.clip(lip[k].astype(np.float32) + dv, 0, 255)
        fr = (l * m + sel[k].astype(np.float32) * (1 - m)).astype(np.uint8)
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait()
    info = {"id": tid, "N": N, "q0": q0, "offsets": {str(int(v)): int((dm == v).sum()) for v in np.unique(dm)},
            "erro_alinh_med": round(float(np.mean(erro)), 2), "erro_alinh_max": round(float(np.max(erro)), 2),
            "landmarks_cobertura": round(cob, 3), "fallback_diferenca": fallback, "dv": [round(float(x), 2) for x in dv],
            "elipse_media": [round(float(x), 1) for x in lm.mean(0)]}
    json.dump(info, open(OUT / f"{tid}.json", "w"), ensure_ascii=False)
    print(json.dumps(info), flush=True)


if __name__ == "__main__":
    for tid in sys.argv[1:]:
        if (OUT / f"{tid}.json").exists() and "--refazer" not in sys.argv:
            continue
        if tid.startswith("--"): continue
        import time as _t
        mp = OUT / f"{tid}.mp4"
        if mp.exists() and _t.time() - mp.stat().st_mtime < 600: continue
        try:
            processar(tid)
        except Exception as e:
            print("ERRO", tid, repr(e), flush=True)

# -*- coding: utf-8 -*-
"""Passo 3 do v2: compara o AD entregue com o v2.
  - md5 do áudio decodificado (tem de ser igual)
  - duração e nº de quadros (tem de ser igual)
  - quadro a quadro: PSNR e pixels com diferença > 40 fora e dentro dos takes refeitos
  - folha com zoom 3x nos takes (entregue x v2), na região onde os dois mais diferem

  python revisar_v2.py ad01 [ad09 ...]   -> _v2_corrigidos/revisao/ADNN_*.jpg + revisao_v2.json
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config_v2 import ADS, LOTE, SAIDA  # noqa: E402

REV = SAIDA / "revisao"


def sh(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout.strip()


def md5_audio(p):
    return sh("ffmpeg", "-v", "error", "-threads", "4", "-i", p, "-map", "0:a", "-f", "md5", "-").replace("MD5=", "")


def info(p):
    d = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p))
    n = int(sh("ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries",
               "stream=nb_read_packets,width,height", "-of", "csv=p=0", p).split(",")[-1])
    ad = sh("ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", p)
    return {"duracao": d, "quadros": n, "dur_audio": float(ad), "mb": round(Path(p).stat().st_size / 2 ** 20, 1)}


def janelas(cfg, ad):
    tre = json.load(open(LOTE / "_trabalho" / ad / "trechos.json", encoding="utf-8-sig"))
    js = []
    for t in tre:
        rel = Path(t["clipe"]).relative_to(LOTE / "_trabalho" / ad).as_posix()
        if rel in cfg["refazer"]:
            i0 = int(round(t["inicio"] * 30))
            js.append((rel, i0, i0 + int(t["quadros"])))
    r = cfg.get("remendo")
    if r and r.get("usar_corrigido"):
        i0 = int(round(r["inicio"] * 30))
        js.append((r["clipe"], i0, i0 + r["quadros"]))
    return js


def psnr(d2):
    m = float(d2.mean())
    return 99.0 if m == 0 else 10 * np.log10(255 ** 2 / m)


def caixa_dif(a, b):
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(2)
    m = (d > 40).astype(np.uint8)
    H, W = d.shape
    fx = m.copy()
    fx[int(H * 0.62):int(H * 0.90)] = 0      # a faixa da legenda não muda no v2: escolhe a região fora dela
    if fx.sum() >= 5:
        m = fx
    if m.sum() < 5:
        cy, cx = H // 2, W // 2
    else:
        m = cv2.dilate(m, np.ones((15, 15), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
        k = 1 + int(np.argmax(st[1:, 4]))
        cx, cy = int(cen[k][0]), int(cen[k][1])
    lado = max(120, H // 8)
    x0 = int(np.clip(cx - lado // 2, 0, W - lado))
    y0 = int(np.clip(cy - lado // 2, 0, H - lado))
    return x0, y0, lado, int((d > 40).sum())


def rotulo(im, txt):
    im = im.copy()
    cv2.rectangle(im, (0, 0), (im.shape[1], 26), (0, 0, 0), -1)
    cv2.putText(im, txt, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    return im


def processar(ad):
    cfg = ADS[ad]
    ent = LOTE / cfg["saida"]
    v2 = SAIDA / (Path(cfg["saida"]).stem + " v2.mp4")
    res = {"entregue": str(ent), "v2": str(v2), "info_entregue": info(ent), "info_v2": info(v2)}
    res["md5_audio_entregue"], res["md5_audio_v2"] = md5_audio(ent), md5_audio(v2)
    res["audio_identico"] = res["md5_audio_entregue"] == res["md5_audio_v2"]
    res["duracao_igual"] = (abs(res["info_entregue"]["duracao"] - res["info_v2"]["duracao"]) < 1e-3
                            and res["info_entregue"]["quadros"] == res["info_v2"]["quadros"])
    js = janelas(cfg, ad)
    res["janelas"] = [[c, a, b, round(a / 30, 3), round(b / 30, 3)] for c, a, b in js]
    alvo = {}
    for c, a, b in js:
        n = b - a
        for f in sorted({a + int(n * 0.2), a + n // 2, a + int(n * 0.8)}):
            alvo[f] = c
    ca, cb = cv2.VideoCapture(str(ent)), cv2.VideoCapture(str(v2))
    fora_psnr, fora_px, den_psnr, den_px = [], [], [], []
    pior_fora = (0, -1)
    pior_den = {}
    guard = {}
    pior_img = {}
    i = 0
    while True:
        oa, a = ca.read()
        ob, b = cb.read()
        if not (oa and ob):
            break
        d = a.astype(np.int16) - b.astype(np.int16)
        d2 = (d.astype(np.int32) ** 2)
        p = psnr(d2)
        px = int((np.abs(d).max(2) > 40).sum())
        dentro = next((c for c, j0, j1 in js if j0 <= i < j1), None)
        if dentro:
            den_psnr.append(p); den_px.append(px)
            if px > pior_den.get(dentro, (-1, 0))[0]:
                pior_den[dentro] = (px, i)
                pior_img[dentro] = (a, b)
        else:
            fora_psnr.append(p); fora_px.append(px)
            if px > pior_fora[0]:
                pior_fora = (px, i)
        if i in alvo:
            guard[i] = (a, b)
        i += 1
    for c, (px, f) in pior_den.items():   # garante o quadro de maior diferença de cada take na folha
        alvo.setdefault(f, c)
        guard.setdefault(f, pior_img[c])
    res["quadros_comparados"] = i
    res["fora_dos_takes"] = {"quadros": len(fora_psnr), "psnr_min": round(min(fora_psnr), 2),
                             "psnr_medio": round(float(np.mean(fora_psnr)), 2),
                             "px40_max": int(max(fora_px)), "px40_medio": round(float(np.mean(fora_px)), 2),
                             "quadro_px40_max": pior_fora[1], "t_px40_max": round(pior_fora[1] / 30, 2)}
    if den_psnr:
        res["dentro_dos_takes"] = {"quadros": len(den_psnr), "psnr_medio": round(float(np.mean(den_psnr)), 2),
                                   "px40_medio": round(float(np.mean(den_px)), 1), "px40_max": int(max(den_px))}
    # parte 1 antiga x parte 1 v2 (antes da compressão final, sem o ruído do encode a 900 kbps)
    from config_v2 import OLD, V2
    pa, pb = cv2.VideoCapture(str(OLD / ad / cfg["hook_old"])), cv2.VideoCapture(str(V2 / ad / cfg["hook_old"]))
    pf, pfi, pd = [], [], []
    k = 0
    while True:
        oa, a = pa.read()
        ob, b = pb.read()
        if not (oa and ob):
            break
        px = int((np.abs(a.astype(np.int16) - b.astype(np.int16)).max(2) > 40).sum())
        if any(j0 <= k < j1 for _, j0, j1 in js):
            pd.append(px)
        else:
            pf.append(px); pfi.append(k)
        k += 1
    j = int(np.argmax(pf))
    res["parte1_fora_dos_takes"] = {"quadros": len(pf), "px40_max": int(pf[j]), "t_px40_max": round(pfi[j] / 30, 2),
                                    "quadros_com_px40>50": int(sum(1 for x in pf if x > 50))}
    res["parte1_dentro_dos_takes"] = {"quadros": len(pd), "px40_medio": round(float(np.mean(pd)), 1) if pd else 0}
    # folha zoom 3x
    REV.mkdir(parents=True, exist_ok=True)
    linhas = []
    for f in sorted(alvo):
        if f not in guard:
            continue
        a, b = guard[f]
        x0, y0, L, npx = caixa_dif(a, b)
        za = cv2.resize(a[y0:y0 + L, x0:x0 + L], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        zb = cv2.resize(b[y0:y0 + L, x0:x0 + L], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        Z = za.shape[0]
        th = []
        for im in (a, b):
            t = im.copy()
            cv2.rectangle(t, (x0, y0), (x0 + L, y0 + L), (0, 255, 255), 3)
            th.append(cv2.resize(t, (int(Z * im.shape[1] / im.shape[0]), Z)))
        nome = Path(alvo[f]).stem.replace("_final", "")
        linhas.append(np.hstack([rotulo(th[0], f"ENTREGUE {nome} t={f / 30:.2f}s"), rotulo(za, "entregue zoom 3x"),
                                 rotulo(zb, f"v2 zoom 3x ({npx} px dif)"), rotulo(th[1], "V2")]))
    if linhas:
        w = max(l.shape[1] for l in linhas)
        linhas = [np.pad(l, ((0, 6), (0, w - l.shape[1]), (0, 0))) for l in linhas]
        folha = np.vstack(linhas)
        if folha.shape[1] > 2400:
            folha = cv2.resize(folha, None, fx=2400 / folha.shape[1], fy=2400 / folha.shape[1])
        out = REV / f"{ad.upper().replace('AD', 'AD')}_takes_zoom3x.jpg"
        cv2.imwrite(str(out), folha, [cv2.IMWRITE_JPEG_QUALITY, 88])
        res["folha_zoom"] = str(out)
    (REV / f"{ad}_revisao_v2.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("audio_identico", "duracao_igual", "fora_dos_takes", "parte1_fora_dos_takes",
                                          "parte1_dentro_dos_takes")}, ensure_ascii=False))
    print(json.dumps(res.get("dentro_dos_takes"), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    for ad in sys.argv[1:]:
        processar(ad)

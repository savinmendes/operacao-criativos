# -*- coding: utf-8 -*-
"""Passo 1 do v2: copia a pasta do AD para _v2_trabalho e re-encaixa os takes com defeito com o
encaixar_edit corrigido (mesmos argumentos). Antes, roda a versão antiga (com o bug) nos mesmos arquivos e
compara com o take que entrou no AD entregue: se bater, o caminho é reproduzível.

  python encaixar_v2.py ad01 [ad09 ...]
Saída: _v2_trabalho/adNN/encaixe_v2.json com as medidas.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config_v2 import ADS, NAO_LISTADOS, OLD, V2, KIT  # noqa: E402

GRANDES_OK = {"base.mp4", "parte2.mp4", "parte1_up.mp4"}


def copiar(ad):
    src, dst = OLD / ad, V2 / ad
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            if f.suffix.lower() == ".mp4" and f.name not in GRANDES_OK:
                continue        # b*.mp4 / parte1*.mp4 / full_up720.mp4: são refeitos ou não são usados
            if not (dst / f.name).exists():
                shutil.copy2(f, dst / f.name)
    for sub in ("flora", "flora2"):
        if (src / sub).is_dir():
            (dst / sub).mkdir(exist_ok=True)
            for f in (src / sub).iterdir():
                if f.is_file() and not (dst / sub / f.name).exists():
                    shutil.copy2(f, dst / sub / f.name)


def encaixar(script, orig, edit, saida, dur):
    a = [sys.executable, str(KIT / script), str(orig), str(edit), str(saida)]
    if dur:
        a += ["--dur", str(dur)]
    r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])
    return r.stdout.strip().splitlines()[-1]


def quadros(p):
    c = cv2.VideoCapture(str(p))
    q = []
    while True:
        ok, im = c.read()
        if not ok:
            break
        q.append(im)
    return q


def medir(a, b):
    """a, b: listas de quadros. Devolve dif. média total, dif. média dentro da faixa da legenda e
    pixels > 40 de diferença fora da faixa (máx/média por quadro)."""
    n = min(len(a), len(b))
    H = a[0].shape[0]
    y0, y1 = int(H * 0.62), int(H * 0.90)
    tot, den, fora = [], [], []
    for x, y in zip(a[:n], b[:n]):
        d = np.abs(x.astype(np.int16) - y.astype(np.int16)).max(2)
        tot.append(float(d.mean()))
        den.append(float(d[y0:y1].mean()))
        f = np.concatenate([d[:y0].ravel(), d[y1:].ravel()])
        fora.append(int((f > 40).sum()))
    return {"quadros": [len(a), len(b)], "dif_media": round(float(np.mean(tot)), 3),
            "dif_media_max_quadro": round(float(np.max(tot)), 3), "dentro_faixa_media": round(float(np.mean(den)), 3),
            "fora_px40_max": int(np.max(fora)), "fora_px40_media": round(float(np.mean(fora)), 1)}


def processar(ad):
    cfg = ADS[ad]
    P = V2 / ad
    copiar(ad)
    res = {"refeitos": {}, "conferidos": {}}
    for clip, (orig, edit, dur) in cfg["refazer"].items():
        fin = P / clip
        v1 = fin.with_name(fin.stem + "_v1.mp4")          # o take que entrou no AD entregue
        shutil.copy2(OLD / ad / clip, v1)
        chk = fin.with_name(fin.stem + "_bugcheck.mp4")
        log_chk = encaixar("encaixar_edit_antigo_bug.py", P / orig, P / edit, chk, dur)
        log_fix = encaixar("encaixar_edit.py", P / orig, P / edit, fin, dur)
        q1, qc, qf = quadros(v1), quadros(chk), quadros(fin)
        res["refeitos"][clip] = {"args": [orig, edit, dur], "log": log_fix,
                                 "reproduz_antigo": medir(q1, qc), "v2_vs_entregue": medir(q1, qf)}
        print(ad, clip, json.dumps(res["refeitos"][clip], ensure_ascii=False), flush=True)
    extra = dict(NAO_LISTADOS.get(ad, {}))
    if cfg.get("remendo"):
        r = cfg["remendo"]
        extra[r["clipe"]] = (r["orig"], r["edit"], r["dur"])
    for clip, (orig, edit, dur) in extra.items():
        fin = P / clip
        fx = fin.with_name(fin.stem + "_fixcheck.mp4")
        encaixar("encaixar_edit.py", P / orig, P / edit, fx, dur)
        res["conferidos"][clip] = {"args": [orig, edit, dur], "corrigido_vs_entregue": medir(quadros(OLD / ad / clip),
                                                                                          quadros(fx))}
        print(ad, clip, "(não listado)", json.dumps(res["conferidos"][clip], ensure_ascii=False), flush=True)
    (P / "encaixe_v2.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    for ad in sys.argv[1:]:
        processar(ad)

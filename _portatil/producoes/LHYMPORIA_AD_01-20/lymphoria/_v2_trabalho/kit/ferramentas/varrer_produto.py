# -*- coding: utf-8 -*-
"""Varre vídeos atrás de um produto (rótulo) e estima quantos takes precisam de troca.
Usa moldes (recortes do rótulo) em várias escalas, amostrando 2 quadros/s, e agrupa por cena.

  python varrer_produto.py --moldes m1.png m2.png --saida varredura.json video1.mp4 video2.mp4 ...

Saída: por vídeo, duração, lista de takes {ini, fim, score} e nº de clipes para editar
(take > 9 s conta como 2+ clipes). Gera também <video>_achados.jpg com 1 quadro por take para conferência.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


def cortes(video, limiar=12):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vf", f"scdet=threshold={limiar},metadata=print",
                        "-an", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ts = []
    for l in r.stderr.splitlines():
        if "lavfi.scd.time=" in l:
            ts.append(float(l.split("lavfi.scd.time=")[-1]))
    return sorted(set(round(t, 3) for t in ts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--moldes", nargs="+", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--limiar", type=float, default=0.66)
    ap.add_argument("videos", nargs="+")
    a = ap.parse_args()
    moldes = [cv2.imread(m, cv2.IMREAD_GRAYSCALE) for m in a.moldes]
    escalas = np.arange(0.55, 1.75, 0.08)
    res = {}
    for v in a.videos:
        cap = cv2.VideoCapture(v)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        dur = n / fps
        passo = max(1, int(round(fps / 2)))
        hits = []
        for i in range(0, n, passo):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ok, im = cap.read()
            if not ok:
                break
            g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            best = 0.0
            for m in moldes:
                for s in escalas:
                    t = cv2.resize(m, None, fx=s, fy=s)
                    if t.shape[0] >= g.shape[0] or t.shape[1] >= g.shape[1]:
                        continue
                    best = max(best, float(cv2.minMaxLoc(cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED))[1]))
            if best >= a.limiar:
                hits.append((i / fps, best))
        cs = [0.0] + cortes(v) + [dur]
        takes = []
        for c0, c1 in zip(cs, cs[1:]):
            h = [s for t, s in hits if c0 <= t < c1]
            if h:
                takes.append({"ini": round(c0, 2), "fim": round(c1, 2), "score": round(max(h), 2)})
        clipes = sum(max(1, int(np.ceil((t["fim"] - t["ini"]) / 9.0))) for t in takes)
        res[Path(v).name] = {"duracao": round(dur, 1), "takes": takes, "clipes": clipes}
        # folha de conferência
        if takes:
            ims = []
            for t in takes[:24]:
                cap.set(cv2.CAP_PROP_POS_MSEC, (t["ini"] + t["fim"]) / 2 * 1000)
                ok, im = cap.read()
                if ok:
                    im = cv2.resize(im, (180, 320))
                    cv2.putText(im, f"{t['ini']:.0f}s", (5, 20), 0, 0.6, (0, 255, 255), 2)
                    ims.append(im)
            while len(ims) % 8:
                ims.append(np.zeros_like(ims[0]))
            rows = [np.hstack(ims[k:k + 8]) for k in range(0, len(ims), 8)]
            cv2.imwrite(str(Path(a.saida).parent / (Path(v).stem + "_achados.jpg")), np.vstack(rows))
        print(f"{Path(v).name}: {dur:.0f}s | takes {len(takes)} | clipes {clipes}", flush=True)
    json.dump(res, open(a.saida, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Parte B (cópia de folha_faixa.py com os takes _b e 5 quadros por take). Folha de conferência da FAIXA DA LEGENDA (62%-90% da altura) nos takes refeitos.
A correção do kit só limpa fora dessa faixa: se o rótulo do produto cair dentro dela, pedaços brancos do
rótulo antigo ainda podem voltar. Mostra lado a lado: edit Kling (quadro aproximado) | take v2.
  python folha_faixa.py ad09 ...   -> _v2_corrigidos/revisao/ADNN_faixa_legenda.jpg
"""
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config_v2 import V2, SAIDA  # noqa: E402
from parteb_v2_b import cfg, b_name  # noqa: E402
ADS = {a: cfg(a) for a in ("ad12", "ad13", "ad19", "ad22")}


def ler(p):
    c = cv2.VideoCapture(str(p))
    q = []
    while True:
        ok, im = c.read()
        if not ok:
            break
        q.append(im)
    return q, c.get(cv2.CAP_PROP_FPS) or 30


for ad in sys.argv[1:]:
    rows = []
    for clip, (orig, edit, dur) in ADS[ad]["refazer"].items():
        fin, _ = ler(V2 / ad / b_name(clip))
        ed, fe = ler(V2 / ad / edit)
        H, W = fin[0].shape[:2]
        y0, y1 = int(H * 0.55), int(H * 0.92)
        for i in sorted({len(fin) // 10, len(fin) * 3 // 10, len(fin) // 2, len(fin) * 7 // 10, len(fin) * 9 // 10}):
            e = cv2.resize(ed[min(len(ed) - 1, int(round(i / 30 * fe)))], (W, H))
            a, b = e[y0:y1], fin[i][y0:y1]
            r = np.hstack([a, np.full((a.shape[0], 6, 3), 255, np.uint8), b])
            r = cv2.resize(r, None, fx=0.75, fy=0.75)
            cv2.putText(r, f"{Path(clip).stem.replace('_final', '')} q{i}  edit Kling | v2", (6, 20), 0, 0.6, (0, 255, 255), 2)
            rows.append(r)
    w = max(r.shape[1] for r in rows)
    rows = [np.pad(r, ((0, 4), (0, w - r.shape[1]), (0, 0))) for r in rows]
    out = SAIDA / "revisao" / f"{ad.upper()}_faixa_legenda.jpg"
    cv2.imwrite(str(out), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(out)

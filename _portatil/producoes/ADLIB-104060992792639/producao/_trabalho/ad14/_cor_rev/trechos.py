# trechos de lipsync (24 fps -> 30 fps do final) + rosto (arg.py) -> trechos.json p/ o _lote/chk_final.py. Uso: python trechos.py adNN
import sys, json, numpy as np
from pathlib import Path
AD = Path(sys.argv[1]); out = []
for s in json.loads((AD / "segmentos.json").read_text())["segmentos"]:
    n = s["nome"]; P = np.load(AD / "lipsync" / "in" / f"geo_{n}.npz")["P"]; P = P[~np.isnan(P).any(axis=(1, 2))]
    x0, y0 = np.percentile(P[:, :, 0].min(1), 5), np.percentile(P[:, :, 1].min(1), 5); x1, y1 = np.percentile(P[:, :, 0].max(1), 95), np.percentile(P[:, :, 1].max(1), 95)
    out.append({"nome": n, "q0": round(s["quadro_ini"] * 30 / 24), "q1": round((s["quadro_fim"] + 1) * 30 / 24) - 1, "rosto": [int(x0 - 20), int(y0 - 20), int(x1 - x0 + 40), int(y1 - y0 + 40)]})
(AD / "_cor_rev" / "trechos.json").write_text(json.dumps(out)); print(len(out))

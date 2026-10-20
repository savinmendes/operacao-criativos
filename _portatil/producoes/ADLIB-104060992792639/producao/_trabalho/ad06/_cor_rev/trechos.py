# trechos de lipsync do AD 06 (24 fps -> 30 fps do final) + rosto (mediana de cx, cy, L do revisor, loteC/escolha_06.json)
# -> _cor_rev/trechos.json p/ o _lote/chk_final.py. w4 e w11 cobertos (close da corda) ficam de fora; w5|w6 divididos em 1135 (47,30 s).
import json, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parent.parent
esc = json.loads((AD.parent / "revisao" / "loteC" / "escolha_06.json").read_text())
cfg = json.loads((AD / "lipsync" / "segs.json").read_text()); out = []
for s in cfg["segs"]:
    n = s["n"]
    if n in ("w4", "w11"): continue
    a, b = s["a"], s["b"]
    if n == "w5": b = 1135
    if n == "w6": a = 1135
    t = np.array([r[1:] for r in esc[n][2]]); cx, cy, L = np.median(t, 0)
    out.append({"nome": n, "q0": round(a * 30 / 24), "q1": round(b * 30 / 24) - 1,
                "rosto": [int(cx - 0.8 * L), int(cy - 1.2 * L), int(1.6 * L), int(1.8 * L)]})
(AD / "_cor_rev" / "trechos.json").write_text(json.dumps(out, indent=0)); print(len(out), out[:2])

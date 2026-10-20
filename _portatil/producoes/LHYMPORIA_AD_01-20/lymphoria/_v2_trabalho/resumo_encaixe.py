# -*- coding: utf-8 -*-
"""Resumo das medidas do encaixe (encaixe_v2.json de cada AD)."""
import json, sys
from pathlib import Path
from config_v2 import ORDEM, V2
for ad in ORDEM:
    p = V2 / ad / "encaixe_v2.json"
    if not p.exists():
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    for c, x in d["refeitos"].items():
        r, v = x["reproduz_antigo"], x["v2_vs_entregue"]
        print(f"{ad} {c:24s} reproduz(dif {r['dif_media']:.2f}, fora40max {r['fora_px40_max']:5d}) | v2 vs entregue fora40 max {v['fora_px40_max']:6d} med {v['fora_px40_media']:8.1f} | q {v['quadros']}")
    for c, x in d["conferidos"].items():
        v = x["corrigido_vs_entregue"]
        print(f"{ad} {c:24s} NAO LISTADO: corrigido vs entregue fora40 max {v['fora_px40_max']:6d} med {v['fora_px40_media']:8.1f} dentro {v['dentro_faixa_media']:.2f} q {v['quadros']}")

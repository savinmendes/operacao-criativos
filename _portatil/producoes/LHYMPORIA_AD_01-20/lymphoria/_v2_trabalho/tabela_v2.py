# -*- coding: utf-8 -*-
"""Tabela (markdown) com o resultado da revisão de cada v2."""
import json
from pathlib import Path
from config_v2 import ORDEM, ADS, SAIDA, V2

print("| AD | Takes refeitos | Áudio (md5) | Duração / quadros | Fora dos takes: parte 1 (px>40 máx) | Fora dos takes: final (PSNR médio / mín) | Dentro dos takes (px>40 médio) | Folha |")
print("|---|---|---|---|---|---|---|---|")
import sys
for ad in (sys.argv[1:] or ORDEM):
    p = SAIDA / "revisao" / f"{ad}_revisao_v2.json"
    if not p.exists():
        print(f"| {ad[2:]} | — | não gerado | | | | | |")
        continue
    r = json.loads(p.read_text(encoding="utf-8"))
    tk = ", ".join(Path(c).stem.replace("_final", "") for c in ADS[ad]["refazer"])
    ie, iv = r["info_entregue"], r["info_v2"]
    p1, f = r["parte1_fora_dos_takes"], r["fora_dos_takes"]
    print(f"| {ad[2:]} | {tk} | {'idêntico' if r['audio_identico'] else 'DIFERENTE'} | "
          f"{'igual' if r['duracao_igual'] else 'DIFERENTE'} ({iv['duracao']:.2f} s, {iv['quadros']} q) | "
          f"{p1['px40_max']} (t={p1['t_px40_max']} s) | {f['psnr_medio']} / {f['psnr_min']} dB | "
          f"{r['parte1_dentro_dos_takes']['px40_medio']} | revisao/{Path(r.get('folha_zoom', '')).name} |")

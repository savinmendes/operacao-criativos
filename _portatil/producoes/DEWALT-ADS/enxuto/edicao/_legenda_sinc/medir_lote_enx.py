# -*- coding: utf-8 -*-
"""Mede a sincronia legenda x fala dos 6 videos do pacote enxuto. Saida: saidas_medicao/<nome>.json + _resumo_sinc.json"""
import json, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import medir_sinc as MS
ED = AQUI.parent
ENT = ED.parent / "entregas"
OUT = AQUI / "saidas_medicao"; OUT.mkdir(exist_ok=True)
nomes = sys.argv[1:] or [c.stem for c in sorted((ED / "cfg_enx").glob("C*.json"))]
rf = AQUI / "_resumo_sinc.json"
resumo = json.load(open(rf, encoding="utf-8")) if rf.exists() else {}
for k, n in enumerate(nomes, 1):
    r = MS.medir(str(ED / "cfg_enx" / f"{n}.json"), str(AQUI / "saidas" / f"{n}.ass"), str(ENT / f"DW7781_{n}.mp4"), n)
    json.dump(r, open(OUT / f"{n}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ruins = [l for l in r["linhas"] if l["erro_ms"] is None or abs(l["erro_ms"]) > 100]
    resumo[n] = {x: r[x] for x in ("blocos_medidos", "blocos_texto_errado", "erro_medio_abs_ms", "erro_max_abs_ms",
                                   "pct_dentro_100ms", "erro_energia_max_abs_ms", "n_energia", "faladas_sem_legenda", "quadros")}
    resumo[n]["fora_100ms"] = ruins
    json.dump(resumo, open(rf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    q = r["quadros"] or {}
    print(f"[{k}/{len(nomes)}] {n}: {r['pct_dentro_100ms']}% <=100ms | max {r['erro_max_abs_ms']} ms | quadros "
          f"{q.get('aparecem_no_quadro_esperado')}/{q.get('eventos_conferidos')} | sem legenda {len(r['faladas_sem_legenda'])} | fora {len(ruins)}", flush=True)
print("FIM")

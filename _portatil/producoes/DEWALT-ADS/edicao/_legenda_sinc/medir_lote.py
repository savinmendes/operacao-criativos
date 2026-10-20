# -*- coding: utf-8 -*-
"""Mede a sincronia legenda x fala de todos os videos entregues DCD7781 (referencia CTC independente do ElevenLabs).
  python medir_lote.py [nome ...]
Saida: saidas_medicao/<nome>.json + _resumo_sinc.json"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import medir_sinc as MS

ED = AQUI.parent
ENT = ED.parent / "entregas"
OUT = AQUI / "saidas_medicao"
OUT.mkdir(exist_ok=True)

itens = []
for c in sorted((ED / "cfg").glob("*_voz.json")):
    n = c.stem[:-4]
    itens.append((f"{n}", c, AQUI / "saidas" / f"{n}_voz.ass", ENT / f"DW7781_{n}.mp4"))
for c in sorted((ED / "cfg").glob("*_fundo.json")):
    n = c.stem[:-6]
    itens.append((f"{n}_fundo-original", c, AQUI / "saidas" / f"{n}_fundo.ass", ENT / f"DW7781_{n}_fundo-original.mp4"))
sel = sys.argv[1:]
if sel:
    itens = [i for i in itens if i[0] in sel]

resumo = {}
rf = AQUI / "_resumo_sinc.json"
if rf.exists() and sel:
    resumo = json.load(open(rf, encoding="utf-8"))
for k, (nome, cfg, ass, video) in enumerate(itens, 1):
    r = MS.medir(str(cfg), str(ass), str(video), nome)
    json.dump(r, open(OUT / f"{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ruins = [l for l in r["linhas"] if l["erro_ms"] is None or abs(l["erro_ms"]) > 100]
    resumo[nome] = {k2: r[k2] for k2 in ("blocos_medidos", "blocos_texto_errado", "erro_medio_abs_ms", "erro_max_abs_ms",
                                         "pct_dentro_100ms", "erro_energia_max_abs_ms", "n_energia")}
    resumo[nome]["faladas_sem_legenda"] = r["faladas_sem_legenda"]
    resumo[nome]["quadros"] = r["quadros"]
    resumo[nome]["fora_100ms"] = ruins
    json.dump(resumo, open(rf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[{k}/{len(itens)}] {nome}: {r['pct_dentro_100ms']}% <=100ms | max {r['erro_max_abs_ms']} ms | "
          f"quadros {r['quadros']['aparecem_no_quadro_esperado'] if r['quadros'] else '-'}/"
          f"{r['quadros']['eventos_conferidos'] if r['quadros'] else '-'} | sem legenda: {len(r['faladas_sem_legenda'])}",
          flush=True)
print("FIM")

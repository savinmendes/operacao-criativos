# -*- coding: utf-8 -*-
"""Gera relatorio.json do lote 3.
A narracao DE tem pausas curtas (escala_pausas 0,7): na maioria dos trechos o checar_lipsync.py nao acha pausa de
>= 8 quadros e nao calcula o indice. Para esses, recalcula o MESMO indice com pausas de >= 4 quadros (borda 1).
status: ok (indice <= 0,6) | aviso (0,6-0,75 ou sem pausa medivel) | usar_broll (> 0,75 ou REPROVADO pelo kit)."""
import json, sys, os
from pathlib import Path
W = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
os.environ.setdefault("GLOG_minloglevel", "2")
import checar_lipsync as C  # noqa: E402

jobs = json.load(open(W / "jobs.json"))
lotes = {t["id"]: t for t in json.load(open(W.parents[1] / "voz" / "lotes.json", encoding="utf-8"))["trechos"]}
C.MIN_Q_PAUSA_RUN, C.BORDA_PAUSA, C.MIN_Q_PAUSA = 4, 1, 4
cache = W / "chk" / "_curto.json"
curto = json.load(open(cache)) if cache.exists() else {}
rel = []
for i in sorted(jobs):
    f = W / "chk" / f"{i}.json"
    if not f.exists():
        rel.append({"id": i, "job_id": jobs[i], "indice": None, "status": "faltando"}); continue
    d = json.load(open(f, encoding="utf-8"))
    idx, metodo = d["indice_pausa"], "kit (pausa >= 8 q)"
    if idx is None:
        if i not in curto:
            r = C.checar(str(W / f"{i}.mp4"), str(W / "in" / f"a_{i}.mp3"), str(W / "base" / f"{i}.mp4"), False)
            curto[i] = {"indice": r.get("indice_pausa"), "n_pausa": r.get("n_pausa"), "status": r.get("status")}
            json.dump(curto, open(cache, "w"), indent=1)
            print(i, curto[i], flush=True)
        idx, metodo = curto[i]["indice"], f"pausa curta >= 4 q ({curto[i]['n_pausa']} q)"
    if d["checar"] == "REPROVADO" and (idx is None or idx > 0.6):
        st = "usar_broll"
    elif idx is None:
        st = "aviso"
    elif idx <= 0.6:
        st = "ok"
    elif idx <= 0.75:
        st = "aviso"
    else:
        st = "usar_broll"
    t = lotes[i]
    rel.append({"id": i, "job_id": jobs[i], "indice": None if idx is None else round(idx, 2), "status": st,
                "metodo_indice": metodo, "checar_kit": d["checar"], "cena": t["cena"],
                "novo_ini": t["novo_ini"], "novo_fim": t["novo_fim"], "quadros": d["quadros"],
                "texto": t["texto"]})
json.dump(rel, open(W / "relatorio.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r["status"] for r in rel))

# -*- coding: utf-8 -*-
"""Junta ids/jobs/medidas em ../relatorio.json."""
import json, glob
from pathlib import Path
AQ = Path(__file__).resolve().parent.parent
TR = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho")
LOT = json.load(open(TR / "voz" / "lotes.json", encoding="utf-8"))
jobs = dict(l.split() for l in open(AQ / "_tmp" / "ids_all.txt") if l.strip())
reenv = {}
p = AQ / "_tmp" / "reenvios.txt"
if p.exists():
    for l in open(p):
        if l.strip():
            t, j = l.split(); reenv.setdefault(t, []).append(jobs.get(t)); jobs[t] = j
med = {}
for f in sorted(glob.glob(str(AQ / "_tmp" / "colar_*.json")), key=lambda f: Path(f).stat().st_mtime):
    med.update(json.load(open(f)))
out = []
for t in LOT["trechos"]:
    if t["lote"] != 1: continue
    tid = t["id"]; r = {"id": tid, "falante": t["falante"], "cena": t["cena"], "novo_ini": t["novo_ini"], "novo_fim": t["novo_fim"]}
    if t["falante"] == "apresentador":
        r.update(job_id=None, indice=None, status="pendente_decisao",
                 obs="nao enviado: apresentador de batina branca com aparencia de Papa (cenas.json pede confirmar com a pessoa); "
                     "lipsync de figura real da Igreja endossando a oferta precisa de decisao explicita da pessoa")
    else:
        m = med.get(tid, {})
        v = m.get("veredito"); r["job_id"] = jobs.get(tid); r["indice"] = m.get("indice"); r["medida"] = m.get("medida")
        r["status"] = {"APROVADO": "ok", "AVISO": "aviso"}.get(v, "usar_broll" if v == "REPROVADO" else "sem_saida")
        if tid in reenv: r["reenvios"] = reenv[tid]
        if m.get("erro"): r["obs"] = m["erro"]
        if (AQ / f"{tid}.mp4").exists(): r["arquivo"] = f"{tid}.mp4"
    out.append(r)
json.dump(out, open(AQ / "relatorio.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r["status"] for r in out))
for r in out:
    if r["status"] not in ("ok", "pendente_decisao"): print(r["id"], r["status"], r.get("indice"), r.get("obs", ""))

# -*- coding: utf-8 -*-
"""Junta blocos ES + textos DE -> roteiro_de.json e mostra a checagem de duracao."""
import json, importlib.util, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
def load(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(AQUI, n + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.DE
DE = {}
for n in ["de_p1", "de_p1b", "de_p2", "de_p3", "de_p4", "de_p5"]:
    if os.path.exists(os.path.join(AQUI, n + ".py")):
        DE.update(load(n))
for n in ["de_p6_enxuto", "de_p7_revisao"]:
    if os.path.exists(os.path.join(AQUI, n + ".py")):
        for k, (de, nt) in load(n).items():
            old = DE.get(k, ("", ""))[1]
            DE[k] = (de, old if nt is None else (old + " " + nt).strip())
ES = json.load(open(os.path.join(AQUI, "blocos_es.json"), encoding="utf-8"))
EXTRA = json.load(open(os.path.join(AQUI, "blocos_extra.json"), encoding="utf-8")) if os.path.exists(os.path.join(AQUI, "blocos_extra.json")) else {}
CORTE = {"B%03d" % i for i in range(23, 34)}
out = []
for b in ES:
    i = b["id"]
    if i in EXTRA:  # correcoes de texto ES / tempos (whisper medium)
        b.update(EXTRA[i])
    de, notas = DE.get(i, ("", "FALTA"))
    item = {"id": i, "ini_es": b["ini_es"], "fim_es": b["fim_es"], "es": b["es"], "de": de, "notas": notas}
    if i in CORTE: item["cortar"] = True
    out.append(item)
# blocos inseridos (ex.: fala nao transcrita pelo whisper small)
for k, v in EXTRA.items():
    if k not in {b["id"] for b in ES}:
        de, notas = DE.get(k, ("", "FALTA"))
        out.append({"id": k, "ini_es": v["ini_es"], "fim_es": v["fim_es"], "es": v["es"], "de": de, "notas": notas})
out.sort(key=lambda x: x["ini_es"])
json.dump(out, open(os.path.join(AQUI, "roteiro_de.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
falt = [o["id"] for o in out if not o["de"]]
mant = [o for o in out if not o.get("cortar")]
wes = sum(len(o["es"].split()) for o in mant); wde = sum(len(o["de"].split()) for o in mant)
dur_es = sum(o["fim_es"] - o["ini_es"] for o in mant)
print(f"blocos {len(out)} (cortados {len(out)-len(mant)}), faltando: {falt}")
print(f"palavras ES (mantidos) {wes} | DE {wde} | fala ES {dur_es/60:.1f} min | DE @150 wpm {wde/150:.1f} min")
if "-v" in sys.argv:
    for o in mant:
        slot = o["fim_es"] - o["ini_es"]; need = len(o["de"].split()) / 150 * 60
        if need > slot * 1.15 + 1:
            print(f"  LONGO {o['id']} slot {slot:.1f}s  DE {need:.1f}s  ({need/slot:.2f}x)")

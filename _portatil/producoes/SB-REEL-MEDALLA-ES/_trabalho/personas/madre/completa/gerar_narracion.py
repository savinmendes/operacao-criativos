# -*- coding: utf-8 -*-
"""Gera <SAIDA>_narracion.txt a partir de mont/palavras_T.json + config.json (série COMPLETA)."""
import json, re, sys
from pathlib import Path
AQ = Path(__file__).resolve().parent
CF = json.loads((AQ / "config.json").read_text(encoding="utf-8"))
W = json.loads((AQ / "mont" / "palavras_T.json").read_text(encoding="utf-8"))
TP = json.loads((AQ / "mont" / "tempos.json").read_text(encoding="utf-8"))
NOME = CF["slug"].upper()
def mmss(t): t = int(t + 0.5); return f"{t // 60:02d}:{t % 60:02d}"
fr, cur = [], []
for w in W:
    if cur and (w.get("parte") != cur[-1].get("parte") or w.get("personagem") != cur[-1].get("personagem")):
        fr.append(cur); cur = []
    cur.append(w)
    if re.search(r"[.!?]$", w["w"]) and not w["w"].endswith("…"):
        fr.append(cur); cur = []
if cur: fr.append(cur)
dur = TP["total"]
L = [f"NARRACIÓN — {CF['saida']} (serie COMPLETA, {int(dur)//60}:{int(dur)%60:02d})",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {NOME} y SACERDOTE (padre). Sello \"VIDEO FICTICIO\" (mini, pegado al borde superior) durante todo el video.",
     "Música propia: tensión grave (gancho y reza) -> tema de esperanza desde la escena del \"después\".",
     f"Voces: {CF['slug']} {CF['voz_nome']} ({CF['voz_id']}) · padre Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).",
     "Botón único: LEARN_MORE (\"Más información\").", ""]
virada = False
for f in fr:
    t = f[0]["ini"]; parte = f[0].get("parte"); txt = " ".join(w["w"] for w in f)
    if parte == "hook" and f is fr[0]:
        L += ["BLOQUE 1 — GANCHO", f"[00:00] ({CF['cena_gancho']})"]
        L.append(f"[{mmss(t)}] {NOME} (voz firme, en off): {txt}"); continue
    if parte == "hook":
        L[-1] += " " + txt; continue
    if parte == "reza":
        txt = re.sub(r",\s+(\w)", lambda m: "… " + m.group(1).lower(), txt)
        if L[-1].startswith(f"[") and "(reza susurrada)" in L[-1]:
            L[-1] = L[-1].rstrip(",") + "… " + txt[0].lower() + txt[1:]
        else:
            L.append(f"[{mmss(t)}] {NOME} (reza susurrada): {txt}")
        continue
    if parte == "selfie" and not virada:
        virada = True
        g0T = TP["G0"] - sum(y - x for x, y in TP["remov"] if y <= TP["G0"])
        L.append(f"[{mmss(g0T)}] ({CF['cena_virada']}, sin voz)")
        L += ["", "BLOQUE 2 — CONEXIÓN", f"[{mmss(t)}] {NOME} (en off; {CF['cena_frustrado']}): {txt}"]; continue
    if f[0].get("personagem") == "sacerdote":
        if "BLOQUE 3" not in "\n".join(L): L += ["", "BLOQUE 3 — MECANISMO Y FUTURO"]
        if txt.lower().startswith("por eso") : L += ["", "BLOQUE 4 — CTA"]
        L.append(f"[{mmss(t)}] PADRE: {txt}"); continue
    L.append(f"[{mmss(t)}] {NOME}: {txt}")
L = [x.replace("<<", "«").replace("...", "…") for x in L]
out = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES") / CF["saida"].replace(".mp4", "_narracion.txt")
out.write_text("\n".join(L) + "\n", encoding="utf-8"); print(out)

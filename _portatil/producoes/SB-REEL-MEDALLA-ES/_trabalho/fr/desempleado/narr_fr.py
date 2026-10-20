# -*- coding: utf-8 -*-
"""Gera NN_SB-FR_<SLUG>_COMPLETA_narracion.txt (FR) a partir de mont/palavras_T.json. uso: python narr_fr.py <pasta fr/slug> <NN> <SLUG> <PERSONAGEM> <voz> <ad.json>"""
import json, sys, re
from pathlib import Path
d = Path(sys.argv[1]).resolve(); nn, nome, pers, voz = sys.argv[2:6]
ad = json.loads(Path(sys.argv[6]).read_text(encoding="utf-8"))
W = json.loads((d / "mont" / "palavras_T.json").read_text(encoding="utf-8"))
W = [w for w in W if re.search(r"\w", w["w"]) or w["w"].startswith("«") or w["w"].startswith("»")]
tot = json.loads((d / "mont" / "tempos.json").read_text())["total"]
fr, cur = [], []
for w in W:
    cur.append(w)
    if re.search(r"[.!?]$", w["w"]) or w is W[-1]:
        fr.append(cur); cur = []
ts = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
txt = lambda c: " ".join(x["w"] for x in c).replace("« ", "« ").replace(" »", " »")
P = lambda p: [c for c in fr if c[0].get("parte") == p and c[0].get("personagem") != "sacerdote"]
pad = [c for c in fr if c[0].get("personagem") == "sacerdote"]
hook, reza, sel = P("hook"), P("reza"), P("selfie")
L = [f"NARRATION — {nn}_SB-FR_{nome}_COMPLETA.mp4 ({int(tot // 60)}:{int(tot % 60):02d})",
     "Temps = début de chaque phrase dans la vidéo finale.",
     f"Personnages fictifs : {pers} et PRÊTRE. Sceau « VIDÉO FICTIVE » (mini, collé en haut à droite) pendant toute la vidéo.",
     "Musique originale : tension grave (accroche et prière) -> thème d'espoir en accords majeurs dès la scène de l'après.",
     f"Voix : {pers.lower()} {voz} · prêtre Alexandre (gP52hjM48hyNoVCbizxO).",
     "Bouton unique : LEARN_MORE (« En savoir plus »).", "",
     "BLOC 1 — ACCROCHE", f"[00:00] ({ad['cena_gancho']})",
     f"[00:00] {pers} (voix ferme, en off) : {' '.join(txt(c) for c in hook)}",
     f"[{ts(reza[0][0]['ini'])}] {pers} (prière murmurée) : {' '.join(txt(c) for c in reza)}",
     f"[{ts(reza[-1][-1]['fim'] + 1)}] ({ad['cena_virada']}, sans voix)", "", "BLOC 2 — CONNEXION"]
for k, c in enumerate(sel):
    L.append(f"[{ts(c[0]['ini'])}] {pers}" + (f" (en off ; {ad['cena_frustrado']})" if k == 0 else "") + f" : {txt(c)}")
L += ["", "BLOC 3 — MÉCANISME ET AVENIR"]
for c in pad:
    if txt(c).startswith("C'est pour ça"): L += ["", "BLOC 4 — CTA"]
    L.append(f"[{ts(c[0]['ini'])}] PRÊTRE : {txt(c)}")
L += ["", "=" * 60, "TEXTE DE L'ANNONCE (FR)", f"Titre ({len(ad['titulo'])} car.) : {ad['titulo']}", "", "Texte principal :", ad["texto"], "",
      "Bouton : En savoir plus"]
out = Path(r"C:\Users\PICHAU\Downloads\SB-MEDALLA-COMPLETA-FR") / f"{nn}_SB-FR_{nome}_COMPLETA_narracion.txt"
out.write_text("\n".join(L) + "\n", encoding="utf-8"); print(out)

# -*- coding: utf-8 -*-
"""Gera NN_SB-FR_<SLUG>_COMPLETA_narracion.txt a partir de mont/palavras_T.json + mont/tempos.json.
Uso: python gerar_narracion_fr.py <pasta_persona_fr> <saida.txt> <ROTULO> <voz_persona> <cena_gancho> <cena_frustre>"""
import json, re, sys
from pathlib import Path

D = Path(sys.argv[1]); OUT = Path(sys.argv[2]); ROT, VOZ, CENA_G, CENA_F = sys.argv[3:7]
W = json.loads((D / "mont" / "palavras_T.json").read_text(encoding="utf-8"))
T = json.loads((D / "mont" / "tempos.json").read_text(encoding="utf-8"))


def mmss(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def frases(ws):
    out, cur = [], []
    for w in ws:
        if not re.search(r"\w", w["w"]) and cur:
            cur[-1] = dict(cur[-1], w=cur[-1]["w"] + " " + w["w"]); continue
        cur.append(w)
        if re.search(r"[.!?]$", w["w"]):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return [(f[0]["ini"], " ".join(x["w"] for x in f).replace("...", "…").replace("« ", "« ")) for f in out]


def parte(p):
    return [w for w in W if w.get("parte") == p and w.get("personagem") != "sacerdote"]


pad = [w for w in W if w.get("personagem") == "sacerdote"]
tot = T["total"]
L = [f"NARRATION — {OUT.name.replace('_narracion.txt', '.mp4')} (série COMPLÈTE, {mmss(tot)})",
     "Temps = début de chaque phrase dans la vidéo finale.",
     f"Personnages fictifs : {ROT} et PRÊTRE. Sceau « VIDÉO FICTIVE » (mini, collé en haut à droite) pendant toute la vidéo.",
     "Musique propre : tension grave (accroche et prière) -> thème d'espoir à partir de la scène de l'« après ».",
     f"Voix : {VOZ} · prêtre Alexandre (gP52hjM48hyNoVCbizxO).",
     "Bouton unique : LEARN_MORE (« En savoir plus »).", "",
     "BLOC 1 — ACCROCHE", f"[00:00] ({CENA_G})"]
for t, f in frases(parte("hook")):
    L.append(f"[{mmss(t)}] {ROT} (voix ferme, en off) : {f}")
for t, f in frases(parte("reza")):
    L.append(f"[{mmss(t)}] {ROT} (prière chuchotée) : {f}")
MC = json.loads((D / "mont" / "mapa_cenas.json").read_text(encoding="utf-8"))
t_dep = next(c["T_ini"] for c in MC if c["fonte"] == "depois.mp4")
L.append(f"[{mmss(t_dep)}] (l'après, sans voix)")
L += ["", "BLOC 2 — CONNEXION"]
for k, (t, f) in enumerate(frases(parte("selfie"))):
    tag = f"(en off ; {CENA_F})" if k == 0 else "(selfie)"
    L.append(f"[{mmss(t)}] {ROT} {tag} : {f}")
fp = frases(pad)
L += ["", "BLOC 3 — MÉCANISME ET FUTUR"]
cta_i = next(i for i, (t, f) in enumerate(fp) if f.startswith("C'est pour ça"))
for t, f in fp[:cta_i]:
    L.append(f"[{mmss(t)}] PRÊTRE : {f}")
L += ["", "BLOC 4 — CTA"]
for t, f in fp[cta_i:]:
    L.append(f"[{mmss(t)}] PRÊTRE : {f}")
L += ["", "TEXTE DE L'ANNONCE",
      "Titre : La médaille de saint Benoît expliquée",
      "Texte principal : Beaucoup de gens portent la médaille de saint Benoît sans savoir ce que disent ses lettres. "
      "Un prêtre les explique, lettre par lettre, dans une transmission en direct ouverte 24 heures sur 24. "
      "Appuie sur « En savoir plus » et viens prier avec nous.",
      "Bouton : En savoir plus (LEARN_MORE)", ""]
OUT.write_text("\n".join(L), encoding="utf-8")
print(OUT)

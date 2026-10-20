# -*- coding: utf-8 -*-
"""Gera o _narracion.txt FR de uma persona a partir de <pasta>/_tmp/mont/palavras_T.json.  uso: python gerar_narracion.py <pasta> <NN>"""
import json, re, sys
from pathlib import Path
P = Path(sys.argv[1]).resolve(); NN = sys.argv[2]
I = json.loads((Path(__file__).parent / "info_narracion.json").read_text(encoding="utf-8"))[P.name]
W = json.loads((P / "_tmp" / "mont" / "palavras_T.json").read_text(encoding="utf-8"))
tp = json.loads((P / "_tmp" / "mont" / "tempos.json").read_text(encoding="utf-8"))
def mmss(t): t = int(t); return f"{t // 60:02d}:{t % 60:02d}"
frases, cur = [], []
for w in W:
    if cur and (cur[-1]["parte"] != w.get("parte") or cur[-1]["personagem"] != w["personagem"]):
        frases.append(cur); cur = []
    cur.append(dict(w, parte=w.get("parte"))); 
    if re.search(r"[.!?…]$|\.\.\.$", w["w"]) or w["w"].endswith("»."):
        frases.append(cur); cur = []
if cur: frases.append(cur)
def txt(f):
    s = " ".join(x["w"] for x in f).replace("...", "…").replace("« ", "«\u00a0").replace(" »", "\u00a0»")
    return re.sub(r"\s+([,.])", r"\1", s)
nome = I["nome"]; slug = I["slug"]
L = [f"NARRATION — {NN}_SB-FR_{slug}_COMPLETA.mp4 (série COMPLÈTE, {mmss(tp['total'] + 0.5)})",
     "Temps = début de chaque phrase dans la vidéo finale.",
     f"Personnages fictifs : {nome} et PRÊTRE. Sceau « VIDÉO FICTIVE » (mini, collé en haut à droite) pendant toute la vidéo.",
     "Musique propre : tension grave (accroche et prière) -> thème d'espoir à partir de la scène de l'« après ».",
     f"Voix : {I['voz_txt']} · prêtre Alexandre (gP52hjM48hyNoVCbizxO).",
     "Bouton unique : LEARN_MORE (« En savoir plus »).", ""]
cab = {"hook": "BLOC 1 — ACCROCHE", "selfie": "BLOC 2 — CONNEXION", "pad1": "BLOC 3 — MÉCANISME ET FUTUR", "cta": "BLOC 4 — CTA"}
L += [cab["hook"], f"[00:00] ({I['cena_gancho']})"]
first_self = True; bloco3 = bloco4 = False
for f in frases:
    p = f[0].get("parte"); t = mmss(f[0]["ini"])
    if f[0]["personagem"] == "sacerdote":
        if not bloco3: L += ["", cab["pad1"]]; bloco3 = True
        if not bloco4 and "C'est pour ça" in txt(f): L += ["", cab["cta"]]; bloco4 = True
        L.append(f"[{t}] PRÊTRE : {txt(f)}"); continue
    if p == "hook": L.append(f"[{t}] {nome} (voix ferme, en off) : {txt(f)}")
    elif p == "reza": L.append(f"[{t}] {nome} (prière chuchotée) : {txt(f)}")
    else:
        if first_self:
            L += [f"[{mmss(tp['T_VIR'] - 0.0)}] (l'après, sans voix)", "", cab["selfie"],
                  f"[{t}] {nome} (en off ; {I['cena_frustrado']}) : {txt(f)}"]; first_self = False
        else: L.append(f"[{t}] {nome} (selfie) : {txt(f)}")
L += ["", "TEXTE DE L'ANNONCE", f"Titre : {I['titulo']}", f"Texte principal : {I['texto']}", "Bouton : En savoir plus (LEARN_MORE)", ""]
out = Path(r"C:\Users\PICHAU\Downloads\SB-MEDALLA-COMPLETA-FR") / f"{NN}_SB-FR_{slug}_COMPLETA_narracion.txt"
out.write_text("\n".join(L), encoding="utf-8"); print(out); print("\n".join(L))

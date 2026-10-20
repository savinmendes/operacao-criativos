# -*- coding: utf-8 -*-
"""Gera <SAIDA>_narracion.txt de uma persona (tempos do vídeo final). python a_narracion.py <slug>"""
import importlib.util, json, re, sys
from pathlib import Path
slug = sys.argv[1]
P = Path(__file__).resolve().parent / slug
spec = importlib.util.spec_from_file_location("m", P / "montar.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
I = json.loads((P / "info.json").read_text(encoding="utf-8"))
W = m.W
fr, cur = [], []
for w in W:
    cur.append(w)
    if re.search(r"[.!?…]$", w["w"]) and not w["w"].endswith("escuchas…") and not w["w"].endswith("..."):
        fr.append(cur); cur = []
if cur: fr.append(cur)
def mmss(t):
    t = int(t); return f"{t // 60:02d}:{t % 60:02d}"
L = [f"NARRACIÓN COMPLETA — {I['saida']} (variación {I['nome']} de la serie Medalla, {mmss(m.TOTAL)[1:]})",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {I['nome']} y SACERDOTE. Sello \"VIDEO FICTICIO\" arriba a la derecha durante todo el video.",
     I["obs"],
     f"Voces: {I['nome'].lower()} {I['voz']} · sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).", ""]
gap_feito = False
for f in fr:
    t = m.S(f[0]["ini"]); quem = I["nome"] if f[0].get("personagem") == "persona" else "SACERDOTE"
    if not gap_feito and f[0]["ini"] >= m.C:
        L.append(f"[{mmss(m.S(m.C) - m.G)}] ({I['virada']}, sin voz)"); gap_feito = True
    extra = f" ({I['abertura']})" if f is fr[0] else ""
    L.append(f"[{mmss(t)}] {quem}{extra}: " + " ".join(w["w"] for w in f))
out = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES") / (I["saida"].replace(".mp4", "_narracion.txt"))
out.write_text("\n".join(L) + "\n", encoding="utf-8"); print(out)

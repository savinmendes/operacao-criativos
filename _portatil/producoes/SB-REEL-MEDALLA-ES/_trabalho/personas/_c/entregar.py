# -*- coding: utf-8 -*-
"""Copia mont/master.mp4 para a pasta de saída com o nome final e gera <nome>_narracion.txt. uso: python entregar.py <slug>"""
import json, re, shutil, sys
from pathlib import Path
AQ = Path(__file__).resolve().parent
slug = sys.argv[1]; P = AQ.parent / slug
sys.path.insert(0, str(P)); import os; os.chdir(P)
import montar as MV
CFG = MV.CFG; OUT = AQ.parents[2]
DESC = {"feria": ("VENDEDORA DE FERIA", "rezando detrás de su puesto vacío, bajo la llovizna", "su puesto con fila de clientes, al sol"),
        "pareja": ("ESPOSA", "rezando de rodillas en su cuarto; su esposo solo en la sala", "los dos riendo juntos en el porche"),
        "pension": ("DUEÑA DE PENSIÓN", "rezando en la recepción, con todas las llaves colgadas", "entrega llaves a huéspedes que llegan con maletas")}
quem, ab, vi = DESC[slug]
def mmss(t): return f"[{int(t // 60):02d}:{int(t % 60):02d}]"
W = MV.W; frases, cur = [], []
for w in W:
    cur.append(w)
    if re.search(r"[.!?…]$", w["w"]) and not w["w"].endswith("…") and not w["w"].endswith(".."):
        frases.append(cur); cur = []
if cur: frases.append(cur)
L = [f"NARRACIÓN COMPLETA — {CFG['saida']}.mp4 (variación {quem} de la v2, {int(MV.TOTAL // 60)}:{int(MV.TOTAL % 60):02d})",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {quem} y SACERDOTE. Sello \"VIDEO FICTICIO\" arriba a la derecha durante todo el video. Sin marcas ni logos.",
     f"Voces: {quem.lower()} {CFG['voz_nome']} ({CFG['voz']}) · sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).", ""]
for f in frases:
    t = MV.S(f[0]["ini"]); txt = " ".join(x["w"] for x in f)
    pers = "SACERDOTE" if f[0].get("personagem") == "sacerdote" else quem
    extra = f" ({ab})" if f[0]["ini"] < 1 else ""
    L.append(f"{mmss(t)} {pers}{extra}: {txt}")
    if f[-1].get("parte") == "reza" and f is frases[-1] or (f[-1].get("parte") == "reza" and W.index(f[-1]) + 1 < len(W) and W[W.index(f[-1]) + 1].get("parte") == "selfie"):
        L.append(f"{mmss(MV.S(MV.C) - MV.G)} ({vi}, sin voz)")
L.append(f"\nVirada (escena de 'después': {vi}) a partir de {mmss(MV.S(MV.VIRA))}.")
dst = OUT / f"{CFG['saida']}.mp4"
shutil.copy2(P / "mont" / "master.mp4", dst)
(OUT / f"{CFG['saida']}_narracion.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print(dst)

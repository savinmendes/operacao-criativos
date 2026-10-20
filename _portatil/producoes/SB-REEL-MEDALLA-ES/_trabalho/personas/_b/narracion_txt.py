# -*- coding: utf-8 -*-
"""Gera <saida>_narracion.txt de uma persona (tempos no vídeo final). Uso: python narracion_txt.py <slug>"""
import json, sys
from pathlib import Path
slug = sys.argv[1]
P = Path(__file__).resolve().parent.parent / slug
sys.path.insert(0, str(P))
import montar as MV

INFO = {
    "costurera": ("COSTURERA", "Gabriela (hHjbwzYZW17oh0p05AKv)",
                  "Costurera de 60 y tantos rezando de rodillas en su taller de noche (máquina quieta, telas sin tocar)",
                  "de día: taller con encargos, ella ajusta el vestido de una clienta, sin voz"),
    "abuela": ("ABUELA", "Grandma Aurora (aYQAm4rWuigkeuRA5i92)",
               "Abuela de 70 y tantos rezando frente a la mesa puesta con las sillas vacías",
               "de día: familia reunida a la mesa, ella sirve la comida, sin voz"),
    "madre": ("MADRE", "Alisson (SmgKjOvC1aIujLWcMzqq)",
              "Madre de 45 rezando de rodillas en la cocina de noche, cuentas sobre la mesa",
              "mañana clara: sus hijos desayunan, ella sonríe, sin voz"),
}
nome, voz, cena_a, cena_d = INFO[slug]
W = MV.W


def ts(t):
    t = int(t); return f"{t // 60:02d}:{t % 60:02d}"


def frases(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if w["w"].rstrip().endswith((".", "!", "?")):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


L = [f"NARRACIÓN COMPLETA — {MV.CFG['saida']} (variación {nome} de la v2, {ts(MV.TOTAL)[1:]})",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {nome} y SACERDOTE. Sello \"VIDEO FICTICIO\" arriba a la derecha durante todo el video.",
     "Sin marcas ni logos.",
     f"Voces: {nome.lower()} {voz} · sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).", ""]
pers = [w for w in W if w.get("fala")]
for k, f in enumerate(frases(pers)):
    tag = f"{nome} (rezando: {cena_a})" if k == 0 else nome
    L.append(f"[{ts(MV.S(f[0]['ini']))}] {tag}: " + " ".join(w["w"] for w in f))
    if f[-1] is MV.fr["f2"][-1]:
        L.append(f"[{ts(MV.S(MV.C) - MV.G)}] ({cena_d})")
for f in frases([w for w in W if not w.get("fala")]):
    L.append(f"[{ts(MV.S(f[0]['ini']))}] SACERDOTE: " + " ".join(w["w"] for w in f))
txt = "\n".join(L) + "\n"
(MV.FINAL.with_name(MV.FINAL.stem + "_narracion.txt")).write_text(txt, encoding="utf-8")
print(txt)

# -*- coding: utf-8 -*-
"""Gera SB-ES_NOTICIA-AURELIO_FICTICIO_narracion.txt (formato dos .txt do lote Medalla)."""
import json, re
from pathlib import Path
import plano
AQ = Path(__file__).resolve().parent
F = {f["id"]: f for f in json.loads((AQ / "voz" / "falas.json").read_text(encoding="utf-8"))}
NOME = {"mujer": "MUJER (react)", "agresor": "AGRESOR", "aurelio": "DON AURELIO", "reportera": "REPORTERA", "sacerdote": "SACERDOTE"}
TXT = {"L09b": "Crux, Lux, Fides, Ignes, Veritas, Silentium, Gladius, Fortitudo, Custodia, Sanctitas, Spiritus y Triumphus.",
       "L10": None}
def mmss(t): return f"{int(t // 60):02d}:{int(t % 60):02d}"
lin = []
for i, d in plano.LIN.items():
    t = TXT.get(i) or F[i]["t"]
    t = t.replace("novecientos dieciocho", "918").replace("cuatrocientos noventa y siete", "497")
    # quebra por frase, com o tempo de início de cada frase
    P = d["palavras"]; frases = re.split(r"(?<=[.!?…:])\s+", t); k = 0
    for fr in frases:
        n = len(fr.split()); n_alin = len([w for w in fr.replace("918", "a b").replace("497", "a b c d").split()])
        ini = d["T0"] + P[min(k, len(P) - 1)]["ini"]; k += n_alin
        rot = NOME[d["p"]] + (" (oración)" if i in ("L09", "L09b") else "") + (" (voz en off)" if i in ("L04",) and False else "")
        lin.append(f"[{mmss(ini)}] {rot}: {fr}")
total = plano.TOTAL
cab = f"""NARRACIÓN COMPLETA — SB-ES_NOTICIA-AURELIO_FICTICIO.mp4 ({int(total // 60)}:{int(total % 60):02d})
Tiempos = momento en que empieza cada frase en el video final.
Personajes ficticios: MUJER (react), AGRESOR, DON AURELIO (vendedor), REPORTERA y SACERDOTE (P. Andrés Molina). Sello "VIDEO FICTICIO" arriba a la derecha durante todo el video.
Voces (ElevenLabs): mujer Karly (sM4f2a6lmttmqTug8V7W) · agresor Richard (Cpm6N9BNC1M75bYS7kO1) · don Aurelio Santiago (VXZKNah1ssrzM8c81OiY) · reportera Gabriela (hHjbwzYZW17oh0p05AKv) · sacerdote Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).
Origen: TESTE1.mp4 (PT-BR) adaptado a español LATAM. Lipsync HeyGen (modo speed) en mujer, reportera, don Aurelio y sacerdote.
"""
out = AQ.parent / "SB-ES_NOTICIA-AURELIO_FICTICIO_narracion.txt"
out.write_text(cab + "\n" + "\n".join(lin) + "\n", encoding="utf-8")
print(out.read_text(encoding="utf-8"))

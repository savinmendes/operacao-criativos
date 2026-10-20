# -*- coding: utf-8 -*-
"""Gera SB-ES_<SLUG>_COMPLETA_narracion.txt (tempos do vídeo final). Uso: python narracion.py <slug>"""
import json, re, sys
from pathlib import Path
slug = sys.argv[1]
P = Path(__file__).resolve().parent.parent / slug / "completa"
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(P))
import montar_completa as MC  # noqa
INFO = {
    "campesino": ("CAMPESINO", "Salvatore (wfTWLJ20rcMqvU8gIiAB)",
                  "plano amplio: él de rodillas en medio de la plantación seca, tierra agrietada",
                  "lluvia sobre la plantación verde: él con los brazos abiertos",
                  "él de pie en la cerca, mirando el campo seco, con el sombrero en la mano"),
    "desempleado": ("DESEMPLEADO", "Alberto Rodríguez (l1zE9xgNpUTaQCZzpNJa)",
                    "plano medio-abierto: él solo en un banco de una plaza casi vacía, rezando con la carpeta en las piernas",
                    "en una oficina: estrecha la mano de una gerente, sonriendo",
                    "en la misma plaza, mirando la carpeta de currículums y el celular sin llamadas"),
}
nome, voz, c_gancho, c_virada, c_frust = INFO[slug]
W = json.loads((MC.M / "palavras_T.json").read_text(encoding="utf-8"))
T = json.loads((MC.M / "tempos.json").read_text())


def ts(t):
    t = int(t + 0.5); return f"{t // 60:02d}:{t % 60:02d}"


def frases(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if re.search(r"[.!?]$", w["w"]) and not re.search(r"(\.\.\.|…)$", w["w"]):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [(f[0]["ini"], " ".join(x["w"] for x in f)) for f in out]


por = lambda parte: [w for w in W if w.get("parte") == parte]
pad = [w for w in W if w.get("personagem") in ("padre", "sacerdote")]
L = [f"NARRACIÓN — SB-ES_{nome}_COMPLETA.mp4 ({ts(T['total'])}) · formato del Medalla COMPLETA",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {nome} y SACERDOTE (padre). Sello \"VIDEO FICTICIO\" (mini, pegado al borde superior) durante todo el video.",
     "Música propia: tensión grave (gancho y reza) -> tema de esperanza desde la virada.",
     f"Voces: {nome.lower()} {voz} · padre Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).",
     "Botón único: LEARN_MORE (\"Más información\").", "", "BLOQUE 1 — GANCHO", f"[00:00] ({c_gancho})"]
L += [f"[{ts(a)}] {nome} (voz firme, en off): {t}" for a, t in frases(por("hook"))]
rz = por("reza")
L.append(f"[{ts(rz[0]['ini'])}] {nome} (reza susurrada): " + " ".join(w["w"] for w in rz))
L.append(f"[{ts(MC.S(MC.C))}] ({c_virada}, sin voz)")
L += ["", "BLOQUE 2 — CONEXIÓN"]
fs = frases(por("selfie"))
L.append(f"[{ts(fs[0][0])}] {nome} (en off; {c_frust}): {fs[0][1]}")
L += [f"[{ts(a)}] {nome} (selfie): {t}" for a, t in fs[1:]]
fp = frases(pad)
k = next(i for i, (a, t) in enumerate(fp) if t.startswith("Por eso"))
L += ["", "BLOQUE 3 — MECANISMO Y FUTURO"] + [f"[{ts(a)}] PADRE: {t}" for a, t in fp[:k]]
L += ["", "BLOQUE 4 — CTA"] + [f"[{ts(a)}] PADRE: {t}" for a, t in fp[k:]]
L = [x.replace("<<", "«") for x in L]
out = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES") / f"SB-ES_{nome}_COMPLETA_narracion.txt"
out.write_text("\n".join(L) + "\n", encoding="utf-8")
print(out)

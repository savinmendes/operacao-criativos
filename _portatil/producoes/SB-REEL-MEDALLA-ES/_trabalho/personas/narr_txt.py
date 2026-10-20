# gera <saida>_narracion.txt a partir de mont/palavras_T.json. uso: python narr_txt.py <pasta completa> <NOME> <PERSONAGEM> <voz> <desc_json>
import json, sys, re
from pathlib import Path
d = Path(sys.argv[1]).resolve(); nome, pers, voz = sys.argv[2], sys.argv[3], sys.argv[4]
desc = json.loads(Path(sys.argv[5]).read_text(encoding="utf-8"))
W = json.loads((d / "mont" / "palavras_T.json").read_text(encoding="utf-8"))
tot = json.loads((d / "mont" / "tempos.json").read_text())["total"]
fr, cur = [], []
for w in W:
    cur.append(w)
    if re.search(r"[.!?]$", w["w"]) or (w is W[-1]):
        fr.append(cur); cur = []
def ts(t): return f"{int(t//60):02d}:{int(t%60):02d}"
def txt(c): return " ".join(x["w"] for x in c)
P = lambda p: [c for c in fr if c[0].get("parte") == p]
pad = [c for c in fr if c[0].get("personagem") == "sacerdote"]
hook, reza, sel = P("hook"), P("reza"), P("selfie")
L = [f"NARRACIÓN — SB-ES_{nome}_COMPLETA.mp4 ({ts(tot).lstrip('0')})",
     "Tiempos = momento en que empieza cada frase en el video final.",
     f"Personajes ficticios: {pers} y SACERDOTE (padre). Sello \"VIDEO FICTICIO\" (mini, pegado al borde superior, a la derecha) durante todo el video.",
     "Música propia: tensión grave (gancho y reza) -> tema de esperanza en acordes mayores desde la escena del después.",
     f"Voces: {pers.lower()} {voz} · padre Pa Gabriel (Zkg9LlmGNlBWLgWjzTnu).",
     "Botón único: LEARN_MORE (\"Más información\").", "",
     "BLOQUE 1 — GANCHO", f"[00:00] ({desc['gancho']})",
     f"[00:00] {pers} (voz firme, en off): {' '.join(txt(c).replace("<<","«") for c in hook)}",
     f"[{ts(reza[0][0]['ini'])}] {pers} (reza susurrada): {' '.join(txt(c) for c in reza)}",
     f"[00:10] ({desc['virada']}, sin voz)", "", "BLOQUE 2 — CONEXIÓN"]
for k, c in enumerate(sel):
    L.append(f"[{ts(c[0]['ini'])}] {pers}" + (f" (en off; {desc['frustrado']})" if k == 0 else "") + f": {txt(c)}")
L += ["", "BLOQUE 3 — MECANISMO Y FUTURO"]
for c in pad:
    if txt(c).startswith("Por eso"): L += ["", "BLOQUE 4 — CTA"]
    L.append(f"[{ts(c[0]['ini'])}] PADRE: {txt(c).replace("<<", "«")}")
out = d.parents[3] / f"SB-ES_{nome}_COMPLETA_narracion.txt"
out.write_text("\n".join(L) + "\n", encoding="utf-8"); print(out)

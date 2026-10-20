# -*- coding: utf-8 -*-
"""Falas ElevenLabs do P4 Julio (reportera Gabriela + Julio Alberto Rodriguez). Uso: python voz.py [ids...]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
AQ = Path(__file__).resolve().parent
GAB, JUL = "hHjbwzYZW17oh0p05AKv", "l1zE9xgNpUTaQCZzpNJa"
F = [
 dict(id="R00", v=GAB, est=0.5, sty=0.2, vel=1.16, t="Imágenes impactantes: un albañil fue humillado por el dueño de la obra… por su fe."),
 dict(id="R01", v=GAB, est=0.5, sty=0.2, vel=1.08, t="Al día siguiente, a don Julio le ofrecieron la obra más grande de su vida."),
 dict(id="R02", v=GAB, est=0.4, sty=0.4, vel=1.06, t="¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
 dict(id="J1", v=JUL, est=0.45, sty=0.3, vel=1.04, t="Esa noche volví caminando a casa, con las manos vacías después de un mes de trabajo."),
 dict(id="J2", v=JUL, est=0.45, sty=0.3, vel=1.04, t="Ya no sabía qué decirle a mi esposa. Mi hermano me mandó la transmisión del padre Juan Méndez."),
 dict(id="J3", v=JUL, est=0.45, sty=0.3, vel=1.04, t="La hice esa misma noche, como él enseña. Al otro día, me llamó un ingeniero que había visto el video."),
 dict(id="P1", v=JUL, est=0.45, sty=0.3, vel=1.04, t="Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche."),
 dict(id="P2", v=JUL, est=0.45, sty=0.3, vel=1.04, t="Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…"),
 dict(id="P3", v=JUL, est=0.45, sty=0.3, vel=1.04, t="y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?"),
]
ids = sys.argv[1:]
tot = 0
for f in F:
    if ids and f["id"] not in ids: continue
    gerar(f["t"], str(AQ / f"{f['id']}.mp3"), f["v"], "eleven_multilingual_v2", f["est"], 0.75, f["sty"], f["vel"])
    tot += len(f["t"]); print("ok", f["id"])
(AQ / "falas.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
print("caracteres", tot, "US$", round(tot / 1000 * 0.165, 3))

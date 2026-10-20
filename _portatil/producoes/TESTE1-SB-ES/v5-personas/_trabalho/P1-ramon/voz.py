# -*- coding: utf-8 -*-
"""Falas ElevenLabs do P1 Ramón (reportera Gabriela + Ramón Salvatore). Uso: python voz.py [ids]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
A = Path(__file__).resolve().parent / "audio"; A.mkdir(exist_ok=True)
GAB, RAM = "hHjbwzYZW17oh0p05AKv", "wfTWLJ20rcMqvU8gIiAB"
PED = ("Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche. "
       "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito… "
       "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?")
F = {
 "R00": (GAB, .5, .2, 1.2, "Imágenes impactantes: un taxista fue humillado por un pasajero… por su fe."),
 "R01": (GAB, .5, .2, 1.12, "Al día siguiente, el taxi de don Ramón no paró ni un minuto."),
 "RA1": (RAM, .45, .3, 1.13, "Esa noche me quedé dentro del taxi, sin ganas de volver a casa. Llevaba semanas haciendo dos carreras por día… no alcanzaba ni para la gasolina."),
 "RA2": (RAM, .45, .3, 1.13, "Mi hija me mandó la transmisión del padre Juan Méndez. La hice ahí mismo, en el taxi, como él enseña. Al otro día, el teléfono empezó a sonar a las seis de la mañana."),
 "PED": (RAM, .45, .3, 1.13, PED),
 "CTA": (GAB, .4, .4, 1.1, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
}
for k in (sys.argv[1:] or F):
    v, e, s, vel, t = F[k]
    if (A / f"{k}.mp3").exists(): continue
    gerar(t, str(A / f"{k}.mp3"), v, "eleven_multilingual_v2", e, 0.75, s, vel); print("ok", k)
json.dump({k: dict(voz=v, est=e, estilo=s, vel=vel, texto=t) for k, (v, e, s, vel, t) in F.items()}, open(A / "falas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

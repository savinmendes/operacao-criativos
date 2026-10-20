# -*- coding: utf-8 -*-
"""TTS ElevenLabs das falas do P6 (Ernesto = Jose lQFpy8cEH4bDaHre2DpA; reportera = Gabriela). Uso: python gen_voz.py [ids]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
AQ = Path(__file__).resolve().parent
ERN, GAB = "lQFpy8cEH4bDaHre2DpA", "hHjbwzYZW17oh0p05AKv"
F = {
 "R00": (GAB, .5, .2, 1.16, "Imágenes impactantes: un mesero fue humillado frente a todo un restaurante… por su fe."),
 "R01": (GAB, .5, .2, 1.08, "Al día siguiente, los clientes hacían fila para que don Ernesto los atendiera."),
 "RCTA": (GAB, .5, .2, 1.08, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
 "E1": (ERN, .45, .3, 1.06, "Esa noche me encerré en el baño del restaurante, con vergüenza de que mis compañeros me vieran llorar."),
 "E2": (ERN, .45, .3, 1.06, "A mi edad, sentía que ya no servía para nada."),
 "E3": (ERN, .45, .3, 1.06, "Un compañero me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña."),
 "E4": (ERN, .45, .3, 1.06, "Al otro día, el dueño me llamó para ofrecerme ser encargado."),
 "P1": (ERN, .45, .3, 1.06, "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche."),
 "P2": (ERN, .45, .3, 1.06, "Es que, igual que yo, lo estabas pidiendo de la forma equivocada."),
 "P3": (ERN, .45, .3, 1.06, "El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito… y está haciendo la oración en vivo ahora mismo."),
 "P4": (ERN, .45, .3, 1.06, "¿Usted puede pasar la transmisión para los que nos están viendo?"),
}
if __name__ == "__main__":
    ids = sys.argv[1:] or list(F)
    for i in ids:
        v, est, sty, vel, t = F[i]
        gerar(t, str(AQ / f"{i}.mp3"), voz=v, estabilidade=est, estilo=sty, velocidade=vel); print("ok", i)
    json.dump({k: dict(voz=v[0], est=v[1], estilo=v[2], vel=v[3], texto=v[4]) for k, v in F.items()}, open(AQ / "falas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

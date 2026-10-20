# -*- coding: utf-8 -*-
"""TTS ElevenLabs das falas da P3 Carmen + reportera. Uso: python tts.py [ids...]"""
import sys, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
AQ = Path(__file__).resolve().parent
GAB, ALI = "hHjbwzYZW17oh0p05AKv", "SmgKjOvC1aIujLWcMzqq"
F = {
 "R00": (GAB, .5, .2, 1.2, "Imágenes impactantes: una empleada fue echada a la calle… por su fe."),
 "R01": (GAB, .5, .2, 1.08, "A los pocos días, Carmen tenía tres familias queriendo contratarla."),
 "CTA": (GAB, .45, .3, 1.08, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
 "C": (ALI, .45, .3, 1.12, "Esa noche pensé en mis hijos y no sabía cómo decirles que me habían echado… y encima acusada de ladrona. Una amiga me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña. Al día siguiente, me llamaron para un trabajo nuevo, con gente que me trata como familia."),
 "P": (ALI, .45, .3, 1.12, "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche. Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito… y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?"),
}
ids = sys.argv[1:] or list(F)
n = 0
for i in ids:
    v, e, s, vel, t = F[i]; n += len(t)
    gerar(t, str(AQ / f"{i}.mp3"), voz=v, estabilidade=e, estilo=s, velocidade=vel)
    print("ok", i)
print("caracteres", n)

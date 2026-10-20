# -*- coding: utf-8 -*-
import sys, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
from pathlib import Path
AQ = Path(__file__).resolve().parent
GAB = "hHjbwzYZW17oh0p05AKv"; MAR = "HRi5Prm2B3PevwpDmVLP"
F = [
 ("R00", GAB, .5, .2, 1.18, "Imágenes impactantes: una feriante fue atacada en plena feria… por su fe."),
 ("R01", GAB, .5, .2, 1.08, "Al día siguiente, el puesto de doña Marta se quedó sin fruta antes del mediodía."),
 ("CTA", GAB, .45, .35, 1.06, "¡Claro! Toquen el botón que está abajo del video y entren ahora a la oración en vivo."),
 ("M1", MAR, .45, .3, 1.04, "Esa noche tiré a la basura la fruta que se me había podrido… igual que todas las semanas. Ya no sabía qué hacer."),
 ("M2", MAR, .45, .3, 1.04, "Mi vecina me mandó la transmisión del padre Juan Méndez. La hice esa misma noche, como él enseña. Al otro día, a las ocho ya tenía fila."),
 ("M3", MAR, .45, .3, 1.04, "Si tú también rezas y sientes que nadie te escucha… y que las cosas solo empeoran… no es que Dios no te escuche."),
 ("M4", MAR, .45, .3, 1.04, "Es que, igual que yo, lo estabas pidiendo de la forma equivocada. El padre Juan Méndez me enseñó la forma correcta de pedirle a San Benito…"),
 ("M5", MAR, .45, .3, 1.04, "y está haciendo la oración en vivo ahora mismo. ¿Usted puede pasar la transmisión para los que nos están viendo?"),
]
so = sys.argv[1:]
for i, v, e, s, vel, t in F:
    if so and i not in so: continue
    gerar(t, str(AQ / f"{i}.mp3"), voz=v, estabilidade=e, estilo=s, velocidade=vel)
    print(i, "ok")
json.dump([dict(id=i, voz=v, est=e, estilo=s, vel=vel, t=t) for i, v, e, s, vel, t in F], open(AQ / "falas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

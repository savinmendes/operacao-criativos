import sys, json, requests
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
txt="Esa noche conté las monedas... no alcanzaba ni para el pasaje de vuelta. Me sentí un viejo que ya no le sirve a nadie."
for nome,vid in [("oscarg","sJYGLUA6m2su09XOMEb8"),("anyelo","QGiPma5r94GQsA2OFYoU"),("albeiro","HVD2dHblkFaLh5Hy0HUJ"),("louis","7UEcc2wDVftk45UjyB46")]:
    try: gerar(txt,f"voz/lib_{nome}.mp3",vid,estabilidade=0.45,estilo=0.3); print("ok",nome)
    except SystemExit as e: print(nome,e)

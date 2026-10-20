import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
txt=open("audio/narr_pl.txt",encoding="utf-8").read().strip()
modelo=sys.argv[1] if len(sys.argv)>1 else "eleven_multilingual_v2"; out=sys.argv[2] if len(sys.argv)>2 else "audio/narr_pl.mp3"
vel=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
print(gerar(txt,out,voz="nPczCjzI2devNBz1zQrb",modelo=modelo,velocidade=vel))

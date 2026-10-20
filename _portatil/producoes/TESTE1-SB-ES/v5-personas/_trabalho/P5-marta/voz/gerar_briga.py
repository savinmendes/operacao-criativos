import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
from pathlib import Path
AQ = Path(__file__).resolve().parent
gerar("¡Llama a tu Dios para que te recoja esto!", str(AQ/"B02.mp3"), voz="Cpm6N9BNC1M75bYS7kO1", estabilidade=.25, estilo=.75, velocidade=1.05)
gerar("¡Señor, yo no le hice nada! ¡Pare, por el amor de Dios!", str(AQ/"B03.mp3"), voz="HRi5Prm2B3PevwpDmVLP", estabilidade=.3, estilo=.65, velocidade=1.04)

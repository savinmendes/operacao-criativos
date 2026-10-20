# gera TTS com alinhamento usando o tts_elevenlabs do kit
import sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from tts_elevenlabs import gerar
import argparse
a=argparse.ArgumentParser(); a.add_argument("voz"); a.add_argument("texto"); a.add_argument("saida")
a.add_argument("--est",type=float,default=0.45); a.add_argument("--estilo",type=float,default=0.2); a.add_argument("--vel",type=float,default=1.0)
x=a.parse_args()
gerar(x.texto,x.saida,voz=x.voz,estabilidade=x.est,estilo=x.estilo,velocidade=x.vel)
print("ok",x.saida)

import sys, subprocess, soundfile as sf; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
src=sys.argv[1]; x=load(src)
print("orig", metricas(x))
for q in (20,30):
    N,n=perfil_ruido(x,q=q)
    for k,pis in [(1.0,-10),(1.5,-14),(2.0,-18)]:
        y=portao_espectral(x,N,k=k,piso_db=pis,fmin=5000); print("gate q",q,"k",k,"piso",pis, metricas(y))

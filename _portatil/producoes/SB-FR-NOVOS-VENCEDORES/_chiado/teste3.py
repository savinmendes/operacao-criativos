import sys, soundfile as sf; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
src, al = sys.argv[1], sys.argv[2]
x = load(src); pw = palavras(al)
for af in ["volume=30dB,afftdn=nr=12:nf=-50:tn=1,volume=-30dB","volume=30dB,afftdn=nr=20:nf=-45:tn=1,volume=-30dB","volume=30dB,afftdn=nr=30:nf=-40:tn=1,volume=-30dB"]:
    y = load(src, af=af); print(af, metricas(y), len(y)-len(x))
N,_ = perfil_ruido(x, q=35); y = portao_espectral(x, N, k=2.0, piso_db=-18, fmin=5000)
for a,r in [(-55,40),(-50,35),(-45,30)]:
    mk, thr = mascara_fala(y, pw, abs_db=a, rel_db=r); print("gate",a,r,"thr",round(thr,1),"fala%",round(mk.mean()*100,1), metricas(portao_tempo(y,mk)))

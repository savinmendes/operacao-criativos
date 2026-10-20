import sys, soundfile as sf; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
src, al, tag = sys.argv[1], sys.argv[2], sys.argv[3]
x = load(src); pw = palavras(al)
print("orig", metricas(x))
for nome, q, k, pis in [("leve",25,1.2,-10),("medio",30,1.5,-14),("forte",35,2.0,-18)]:
    N,_ = perfil_ruido(x, q=q); y = portao_espectral(x, N, k=k, piso_db=pis, fmin=5000)
    mk, thr = mascara_fala(y, pw); z = portao_tempo(y, mk)
    print(nome, "espectral", metricas(y), "| +gate", metricas(z), "gate thr", round(thr,1), "fala%", round(mk.mean()*100,1))
    sf.write(rf"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado\t_{tag}_{nome}.wav", z, SR)
for af in ["afftdn=nr=12:nf=-70:tn=1", "afftdn=nr=18:nf=-60:tn=1"]:
    y = load(src, af=af); print(af, metricas(y))

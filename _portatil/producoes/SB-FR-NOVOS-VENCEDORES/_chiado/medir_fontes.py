import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
A=r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho\audio"
B=r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\03_ADS-13.13F-REZA-MUJER\_trabalho\audio"
for mp3,al in [(A+r"\corpo_fr.mp3",A+r"\corpo_fr.alinhamento.json"),(A+r"\hook1_fr.mp3",A+r"\hook1_fr.alinhamento.json"),(A+r"\hook2_fr.mp3",A+r"\hook2_fr.alinhamento.json"),(B+r"\fr_raw2.mp3",B+r"\fr_raw2.alinhamento.json"),(B+r"\voz_fr.wav",B+r"\voz_fr_p.alinhamento.json")]:
    x=load(mp3); T=len(x)/SR; pw=palavras(al); P=pausas(pw,total=T)
    print(mp3.split("\\")[-1], round(T,2), "pausas", round(sum(e-s for s,e in P),2),"s", "PAUSA(hi,lo,hi-lo,n)",bandas(x,SR,P),"FALA",bandas(x,SR,fala(pw)))

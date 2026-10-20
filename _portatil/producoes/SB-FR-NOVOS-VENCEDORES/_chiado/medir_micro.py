import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
A=r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho\audio"
B=r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\03_ADS-13.13F-REZA-MUJER\_trabalho\audio"
for mp3,al in [(A+r"\corpo_fr.mp3",A+r"\corpo_fr.alinhamento.json"),(A+r"\hook2_fr.mp3",A+r"\hook2_fr.alinhamento.json"),(B+r"\fr_raw2.mp3",B+r"\fr_raw2.alinhamento.json")]:
    x=load(mp3); pw=palavras(al)
    for mn,mg in [(0.06,0.015),(0.12,0.03),(0.25,0.08)]:
        P=[(a[2]+mg,b[1]-mg) for a,b in zip(pw,pw[1:]) if b[1]-a[2]>=mn]
        P=[(s,e) for s,e in P if e-s>0.045]
        print(mp3.split("\\")[-1],mn,len(P),round(sum(e-s for s,e in P),2),bandas(x,SR,P,nfft=1024))

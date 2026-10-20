import sys; sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
def ads20_pw():
    A=r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho\audio"
    return palavras(A+r"\hook1_fr.alinhamento.json",0.08)+palavras(A+r"\hook2_fr.alinhamento.json",2.45)+palavras(A+r"\corpo_fr_p.alinhamento.json",4.38)
def m13_pw():
    return palavras(r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\03_ADS-13.13F-REZA-MUJER\_trabalho\audio\voz_fr_p.alinhamento.json")
if __name__=="__main__":
    pw={"ADS20":ads20_pw,"1313F":m13_pw}[sys.argv[1]]()
    for f in sys.argv[2:]:
        x=load(f); T=len(x)/SR; P=pausas(pw,total=T)
        print(f.replace("\\","/").split("/")[-1], round(T,2),"pausas",round(sum(e-s for s,e in P),2),"s PAUSA(hi,lo,dif)",bandas(x,SR,P)[:3],"FALA",bandas(x,SR,fala(pw))[:3])

import json
from palavras import palavras
from mapa import O, TOTAL
W=palavras("audio/velho.alinhamento.json",0.05)+palavras("audio/anjo.alinhamento.json",O)
SHOTS=[("V",0,4.60),("A1",5.90,9.30),("A2",9.63,30.70),("C",30.90,34.67),("A3",34.87,41.10),("A4",42.90,44.87),
       ("A5",47.00,53.80),("A6",56.93,74.77),("A7",80.30,98.83),("A8",103.40,TOTAL)]
gaps=[((W[i][2]+W[i+1][1])/2, W[i+1][1]-W[i][2]) for i in range(len(W)-1)]
def q(t): return round(t*30)/30
ch=[]
def split(n,a,b):
    if b-a<=12: ch.append((n,q(a),q(b))); return
    k=max(2,int((b-a)//11.5)+1); L=(b-a)/k; cur=a
    for j in range(1,k):
        alvo=a+j*L
        g=min([g for g in gaps if cur+3<g[0]<b-3 and g[1]>=0.12], key=lambda g: abs(g[0]-alvo)-0.5*g[1])
        ch.append((f"{n}{j}",q(cur),q(g[0]))); cur=g[0]
    ch.append((f"{n}{k}",q(cur),q(b)))
for n,a,b in SHOTS: split(n,a,b)
for c in ch: print(c, round(c[2]-c[1],2), " ".join(w[0] for w in W if c[1]<=w[1]<c[2]))
json.dump(ch,open("chunks.json","w"),indent=0)

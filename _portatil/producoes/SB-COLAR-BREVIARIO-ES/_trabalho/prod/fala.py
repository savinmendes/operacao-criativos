import json
def segs(arq):
    out=[[]]
    for l in open(arq,encoding="utf-8"):
        w,a,b=l.split(); a=float(a); b=float(b)
        if w=="|": out.append([])
        else: out[-1].append((w,a,b))
    return out
S=json.load(open("segs_es.json",encoding="utf-8"))
M=segs("voz/moca_pal.txt"); P=segs("voz/padre_pal.txt")
assert len(M)+len(P)==len(S),(len(M),len(P))
G=M+P
for s,g in zip(S,G):
    s["es_ini"]=g[0][1]; s["es_fim"]=g[-1][2]; s["pal"]=g
if __name__=="__main__":
    tot=0
    for k,s in enumerate(S):
        d=s["es_fim"]-s["es_ini"]; pt=s["b"]-s["a"]
        nxt=S[k+1]["a"] if k+1<len(S) else 139.1
        print(f'{s["i"]:2d} {s["a"]:6.1f} PT {pt:4.1f} ES {d:4.2f} r={d/pt:4.2f} cabe_ate_prox {nxt-s["a"]:4.1f} {"OVER" if d>nxt-s["a"] else ""}')
    json.dump(S,open("segs_es_t.json","w",encoding="utf-8"),ensure_ascii=False)

import json,sys
def palavras(p):
    d=json.load(open(p,encoding='utf-8'));W=[];cur=None
    for ch,s,e in zip(d["characters"],d["character_start_times_seconds"],d["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append(cur); cur=None
            continue
        if cur is None: cur=[ch,s,e]
        else: cur[0]+=ch; cur[2]=e
    if cur: W.append(cur)
    return W
if __name__=="__main__":
    for f in sys.argv[1:]:
        W=palavras(f); print(f, " ".join(f"{w}[{s:.2f}-{e:.2f}]" for w,s,e in W)); 
        print("  gaps>0.25:",[(W[i][0],round(W[i+1][1]-W[i][2],2)) for i in range(len(W)-1) if W[i+1][1]-W[i][2]>0.25])

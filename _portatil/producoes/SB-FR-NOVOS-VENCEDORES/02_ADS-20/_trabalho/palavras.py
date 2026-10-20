import json,sys
def palavras(p,off=0):
    a=json.load(open(p,encoding="utf-8")); ch=a["characters"]; s=a["character_start_times_seconds"]; e=a["character_end_times_seconds"]
    out=[]; cur="";cs=None;ce=None
    for c,a0,a1 in zip(ch,s,e):
        if c.isspace():
            if cur: out.append([cur,cs+off,ce+off]); cur=""
        else:
            if not cur: cs=a0
            cur+=c; ce=a1
    if cur: out.append([cur,cs+off,ce+off])
    return out
if __name__=="__main__":
    for w in palavras(sys.argv[1],float(sys.argv[2]) if len(sys.argv)>2 else 0): print(f"{w[1]:.2f}-{w[2]:.2f} {w[0]}")

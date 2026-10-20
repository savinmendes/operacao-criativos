import json,unicodedata,re,sys
def norm(s): return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
W=[]
for s in json.load(open('whisper.json',encoding='utf-8')): W+=s['w']
W+= [tuple(x) for x in json.load(open('reza_w.json',encoding='utf-8'))]
W=[(a,b,norm(w).strip()) for a,b,w in W]; W.sort()
src=sys.argv[1]
r=json.load(open(src,encoding='utf-8'))
prev='';out=[]
for k,t in r:
    n=norm(t).replace(' ','')
    if not n or n==prev: continue
    prev=n; t0=k/30
    # find whisper word whose text is prefix of n near t0
    best=None
    for a,b,w in W:
        if w and n.startswith(w[:4]) and abs(a-t0)<2.5:
            if best is None or abs(a-t0)<abs(best[0]-t0): best=(a,w)
    if best: out.append((t0,best[0],round(t0-best[0],2),t)) 
    else: out.append((t0,None,None,t))
for x in out:
    flag='  <<<' if x[2] is not None and abs(x[2])>0.2 else ''
    print(f'{x[0]:7.2f} {x[1] if x[1] is None else round(x[1],2)} d={x[2]} {x[3]}{flag}')

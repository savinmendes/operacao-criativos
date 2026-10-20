import json,unicodedata,re,difflib
def n(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r"[^a-z]","",s)
B=json.load(open("../blocos_fr.json",encoding="utf-8"))
W=json.load(open("words.json",encoding="utf-8"))
bt=[];
for i,(a,b,t) in enumerate(B):
    toks=re.split(r"[\s'\-]+",t)
    for j,k in enumerate(toks):
        if n(k): bt.append((i,j,n(k)))
wt=[]
for k,(a,b,w,p) in enumerate(W):
    for x in re.split(r"[\s'\-]+",w):
        if n(x): wt.append((k,n(x)))
sm=difflib.SequenceMatcher(None,[x[2] for x in bt],[x[1] for x in wt],autojunk=False)
mp={}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for d in range(i2-i1): mp[i1+d]=wt[j1+d][0]
    elif tag!='equal': print("DIFF",tag,[x[2] for x in bt[i1:i2]],[x[1] for x in wt[j1:j2]], W[wt[j1][0]][0] if j1<len(wt) else '')
first={}
for idx,(i,j,k) in enumerate(bt):
    if j==0 or i not in first:
        if idx in mp and i not in first: first[i]=mp[idx]
for i,(a,b,t) in enumerate(B):
    if i in first:
        ws=W[first[i]][0]; d=a-ws
        if abs(d)>0.25: print(f"SYNC {t!r} bloco {a:.2f} fala {ws:.2f} desvio {d:+.2f}")
print("blocos",len(B),"ultimo",B[-1])
gaps=[(B[i][1],B[i+1][0]) for i in range(len(B)-1) if B[i+1][0]-B[i][1]>0.3]
print("gaps",gaps)
print("max len",max(B,key=lambda x:len(x[2])))

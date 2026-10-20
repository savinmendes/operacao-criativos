import re,json,unicodedata,statistics
def n(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if c.isalnum())
def ts(s): h,m,x=s.split(':'); return int(h)*3600+int(m)*60+float(x)
d=json.load(open('../revisor/whisper.json',encoding='utf-8'))
W=[(w[0],w[1],n(w[2])) for s in d for w in s['w']]
diffs=[]
for l in open('leg.ass',encoding='utf-8'):
    if not l.startswith('Dialogue'): continue
    p=l.split(',',9)
    if p[3]!='L': continue
    m=re.search(r'&H00FFFF&\}([^{ ]+)',p[9])
    if not m: continue
    w=n(m.group(1)); t=ts(p[1])
    c=[x for x in W if x[2]==w and abs(x[0]-t)<2]
    if not c: continue
    c=min(c,key=lambda x:abs(x[0]-t)); diffs.append((round(t-c[0],2),t,w))
print(len(diffs),'median',statistics.median([x[0] for x in diffs]))
print([x for x in diffs if abs(x[0])>0.25])

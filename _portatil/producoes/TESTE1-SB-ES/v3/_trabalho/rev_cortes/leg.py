import re,json,unicodedata,difflib
def ts(s):
    neg=s.startswith('-');h,m,x=s.lstrip('-').split(':');v=int(h)*3600+int(m)*60+float(x);return -v if neg else v
def nz(w): return ''.join(c for c in unicodedata.normalize('NFD',w.lower()) if c.isalnum() and unicodedata.category(c)!='Mn')
ev=[]
for l in open('../final/mont/leg.ass',encoding='utf8'):
    if not l.startswith('Dialogue'):continue
    p=l.split(',',9);s,e=ts(p[1]),ts(p[2]);txt=p[9].strip()
    m=re.search(r'c&H00FFFF&\}([^{]+)',txt)
    words=re.sub(r'\{[^}]*\}','',txt)
    ev.append((s,e,m.group(1).strip() if m else None,words))
hw=[(s,w) for s,e,w,_ in ev if w]
# whisper words
W=[]
for sg in json.load(open('whisper.json',encoding='utf8')):
    for a,b,w,pr in sg['w']: W.append((a,w.strip()))
A=[nz(w) for _,w in hw];B=[nz(w) for _,w in W]
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
d=[]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1): d.append((hw[i1+k][0],hw[i1+k][1],W[j1+k][0]))
    else: print(tag,'leg',[f'{hw[i][0]:.2f}:{hw[i][1]}' for i in range(i1,i2)][:12],'wh',[f'{W[j][0]:.2f}:{W[j][1]}' for j in range(j1,j2)][:12])
import numpy as np
off=np.array([x[0]-x[2] for x in d]);print('n',len(d),'offset med',np.median(off),'p95 abs',np.percentile(abs(off),95))
big=[(round(a,2),w,round(a-b,2)) for a,w,b in d if abs(a-b)>0.25];print('>0.25s',big)
for t in [5,20,33,45,60,95,115,140,150,160,167]:
    c=min(d,key=lambda x:abs(x[0]-t));print('amostra',round(c[0],2),c[1],'whisper',round(c[2],2),'dif',round(c[0]-c[2],2))
# gaps without subtitle while speech
ev.sort();gaps=[(round(ev[i][1],2),round(ev[i+1][0],2)) for i in range(len(ev)-1) if ev[i+1][0]-ev[i][1]>0.3]
print('gaps',gaps)
print('last event end',ev[-1][1])

import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8')); a=a.get('alignment',a)
c=a['characters']; s=a['character_start_times_seconds']
w='';t0=None;out=[]
for ch,t in zip(c,s):
    if ch.isspace():
        if w: out.append(f'{t0:.1f}:{w}')
        w='';t0=None
    else:
        if t0 is None:t0=t
        w+=ch
if w: out.append(f'{t0:.1f}:{w}')
print(' '.join(out))

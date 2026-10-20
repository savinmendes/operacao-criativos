import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
c=a['characters'];s=a['character_start_times_seconds'];e=a['character_end_times_seconds']
w=[];cur='';st=None
for ch,t0,t1 in zip(c,s,e):
    if ch.isspace():
        if cur: w.append((cur,st,pe)); cur=''
    else:
        if not cur: st=t0
        cur+=ch; pe=t1
if cur: w.append((cur,st,pe))
print(' '.join(f'{x}[{a:.2f}]' for x,a,b in w))

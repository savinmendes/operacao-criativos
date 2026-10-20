import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
c=a['characters'];s=a['character_start_times_seconds'];e=a['character_end_times_seconds']
# words
w=[];cur='';st=None
for ch,t0,t1 in zip(c,s,e):
    if ch.isspace():
        if cur: w.append((cur,st,pe)); cur=''
    else:
        if not cur: st=t0
        cur+=ch; pe=t1
if cur: w.append((cur,st,pe))
for i in range(1,len(w)):
    g=w[i][1]-w[i-1][2]
    if g>0.25: print(f'gap {g:.2f} before "{w[i][0]}" at {w[i][1]:.2f}')
print('words',len(w),'end',w[-1][2])

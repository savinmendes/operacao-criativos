import json,re,sys
for i in sys.argv[1:]:
    al=json.load(open(f'{i}/narr.alinhamento.json',encoding='utf-8'))
    C,S,E=al['characters'],al['character_start_times_seconds'],al['character_end_times_seconds']
    t=''.join(C); print('==',i,len(t))
    for m in re.finditer(r"[^.!?]+[.!?]*",t):
        if not m.group().strip(): continue
        a=m.start(); b=m.end()-1
        while t[a] in ' \n': a+=1
        while b>a and t[b] in ' \n': b-=1
        print(f'{S[a]:6.2f} {E[b]:6.2f} dur {E[b]-S[a]:5.2f}  {t[a:b+1]}')

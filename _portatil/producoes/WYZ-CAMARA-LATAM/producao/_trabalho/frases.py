import json,sys,re
a=json.load(open(sys.argv[1],encoding='utf-8')); a=a.get('alignment',a)
ch=a['characters']; s=a['character_start_times_seconds']; e=a['character_end_times_seconds']
txt=''.join(ch); 
i=0
for m in re.finditer(r'[^.\n]+[.\n]?',txt):
    t=m.group().strip()
    if not t: continue
    st=m.start()+len(m.group())-len(m.group().lstrip()); en=m.end()-1
    while txt[en] in ' \n.' and en>st: en-=1
    print(f"{s[st]:6.2f} {e[en]:6.2f}  {t}")

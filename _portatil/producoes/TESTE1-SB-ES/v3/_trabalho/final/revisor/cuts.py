import json
from tile import tile
tl=json.load(open('../timeline_v3.json',encoding='utf-8'))
cuts=[p['q0'] for p in tl['planos']][1:]+[3443,3913]
cuts=sorted(set(cuts))
for g in range(0,len(cuts),8):
    fr=[]
    for c in cuts[g:g+8]: fr+= [max(0,c-3)+k for k in range(6)]
    tile(fr,6,120,f'cortes_{g//8:02d}.jpg')
print(len(cuts))

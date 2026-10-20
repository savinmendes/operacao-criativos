import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
prev=None
for f in d:
    its=[i for i in f['items'] if 1350<i[1]<1600]
    oth=[i for i in f['items'] if not (1350<i[1]<1600)]
    s=' | '.join(f"{i[2]}({i[3]},x{int(i[4][0])}-{int(i[4][1])},y{int(i[1])})" for i in its)
    o=' || OUTRO: '+' | '.join(i[2] for i in oth) if oth else ''
    key=' '.join(i[2] for i in its)
    if key!=prev: print(f"{f['t']:6.2f} {s}{o}")
    prev=key

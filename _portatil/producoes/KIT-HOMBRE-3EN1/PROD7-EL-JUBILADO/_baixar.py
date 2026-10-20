import json,sys,urllib.request,os
# uso: _baixar.py status.json pasta ext  genid=nome ...
d=json.load(open(sys.argv[1],encoding='utf-8'))
if isinstance(d,list): d=json.loads(d[0]['text'])
pasta,ext=sys.argv[2],sys.argv[3]
ids=dict(a.split('=') for a in sys.argv[4:])
print('all_completed',d['all_completed'],'fail',d['has_failures'])
for g in d['generations']:
    n=ids.get(g['id'],g['id']); print(n,g['status'],g.get('error_message',''))
    out=f'{pasta}/{n}.{ext}'
    if g['status']=='completed' and not os.path.exists(out): urllib.request.urlretrieve(g['content_url'],out)

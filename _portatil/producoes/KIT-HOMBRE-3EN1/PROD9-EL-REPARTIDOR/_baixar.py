import json,sys,urllib.request,os
# uso: python _baixar.py status.json pasta id=nome ...
raw=open(sys.argv[1],encoding='utf-8').read()
d=json.loads(raw)
if isinstance(d,list): d=json.loads(d[0]['text'])
pasta=sys.argv[2]; ids=dict(a.split('=') for a in sys.argv[3:])
print('all_completed',d['all_completed'],'fail',d['has_failures'])
for g in d['generations']:
    n=ids.get(g['id'],g['id']); print(n,g['status'],g.get('error_message',''))
    ext='.png' if g.get('modality')=='image' else '.mp4'
    out=f'{pasta}/{n}{ext}'
    if g['status']=='completed' and not os.path.exists(out): urllib.request.urlretrieve(g['content_url'],out)

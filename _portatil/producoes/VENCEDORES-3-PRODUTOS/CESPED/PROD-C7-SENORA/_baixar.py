import json,sys,urllib.request,os
# uso: python _baixar.py status.json gid=destino ...  (ou id de node)
d=json.load(open(sys.argv[1],encoding='utf-8')) if sys.argv[1].endswith('.json') else None
m=dict(a.split('=',1) for a in sys.argv[2:])
print('all_completed',d.get('all_completed'),'fail',d.get('has_failures'))
for g in d['generations']:
    k=g['id'] if g['id'] in m else g.get('node_id')
    print(g['id'],g.get('node_id'),g['status'],g.get('error_message',''))
    if k in m and g['status']=='completed' and not os.path.exists(m[k]):
        urllib.request.urlretrieve(g['content_url'],m[k]); print(' ->',m[k])

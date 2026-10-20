import json,sys,urllib.request,os
d=json.load(open(sys.argv[1],encoding='utf-8')) if os.path.exists(sys.argv[1]) else json.loads(sys.argv[1])
if isinstance(d,list): d=json.loads(d[0]['text'])
ids=json.loads(sys.argv[2])  # {gen_or_node_id: destino}
print('all_completed',d.get('all_completed'),'fail',d.get('has_failures'))
for g in d['generations']:
    n=ids.get(g['id']) or ids.get(g.get('node_id','')); print(g['id'],g.get('node_id'),n,g['status'],g.get('error_message',''))
    if n and g['status']=='completed' and not os.path.exists(n): urllib.request.urlretrieve(g['content_url'],n); print('baixado',n)

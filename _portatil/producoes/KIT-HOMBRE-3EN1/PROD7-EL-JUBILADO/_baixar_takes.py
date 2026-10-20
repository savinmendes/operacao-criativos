import json,sys,urllib.request,os
d=json.load(open(sys.argv[1],encoding='utf-8'))
if isinstance(d,list): d=json.loads(d[0]['text'])
ids={'cetnVLFjGNnKWllovU2A':'V1_gancho','ptiYnOwTjvEc1Udks4e0':'V2_selfie','Yk632qIHC9GN6wCGqj0w':'V3_dia','U78TbwRtiVUFsCh9Zp0J':'V4_noite'}
print('all_completed',d['all_completed'],'fail',d['has_failures'])
for g in d['generations']:
    n=ids.get(g['id'],g['id']); print(n,g['status'],g.get('error_message',''))
    out=f'takes/{n}.mp4'
    if g['status']=='completed' and not os.path.exists(out): urllib.request.urlretrieve(g['content_url'],out)

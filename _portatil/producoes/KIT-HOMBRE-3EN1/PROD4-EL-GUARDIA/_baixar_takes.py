import json,sys,urllib.request,os
d=json.load(open(sys.argv[1],encoding='utf-8'))
if isinstance(d,list): d=json.loads(d[0]['text'])
ids={'87uVGuCtvxdUevbL5eDo':'V1_gancho','mEG1DgEvOjBz71kl0wHG':'V2_selfie','NTAvHfhGZOkJJH8FjyTA':'V3_dia','W6HbZNdTvSPthrQW3hHR':'V4_noite'}
print('all_completed',d['all_completed'],'fail',d['has_failures'])
for g in d['generations']:
    n=ids.get(g['id'],g['id']); print(n,g['status'],g.get('error_message',''))
    out=f'takes/{n}.mp4'
    if g['status']=='completed' and not os.path.exists(out): urllib.request.urlretrieve(g['content_url'],out)

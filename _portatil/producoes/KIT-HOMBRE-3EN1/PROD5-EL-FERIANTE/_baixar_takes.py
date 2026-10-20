import json,sys,urllib.request,os
d=json.load(open(sys.argv[1],encoding='utf-8'))
ids={'JFYIzIXLR2ZWlPGFodna':'V1_gancho1','AqVSj4qMwUeaiGuXBTt3':'V2_gancho2','dQOEcPmwBqWmz1H32tZo':'V3_selfie','9EBc5fMzCPuVKbitLVGq':'V4_oferta','8Cs0fN5GcS3lm6tqH8Of':'V5_dia','LUO48b5n8K6XYNXJIDRJ':'V6_noite1','p4afu7jhY21ZSfSB0KAs':'V7_noite2','t2fQlNXwjBsRZzEUBuqN':'V8_bar1','hDSr5fmaMqFkDAUT1OZX':'V9_bar2'}
print('all_completed',d['all_completed'],'fail',d['has_failures'])
for g in d['generations']:
    n=ids[g['id']]; print(n,g['status'],g.get('error_message',''))
    out=f'takes/{n}.mp4'
    if g['status']=='completed' and not os.path.exists(out): urllib.request.urlretrieve(g['content_url'],out)

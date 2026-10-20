import sys,re
from curl_cffi import requests
out=set()
for slug in sys.argv[1:]:
    try:
        r=requests.get(f"https://www.tiktok.com/discover/{slug}",impersonate="chrome",timeout=30)
        for m in re.findall(r'(@[\w\.]+)/video/(\d{15,20})',r.text): out.add(f"https://www.tiktok.com/{m[0]}/video/{m[1]}")
        ids=re.findall(r'"id":"(\d{18,20})"',r.text)
        print(slug,r.status_code,len(r.text),len(ids),file=sys.stderr)
    except Exception as e: print(slug,e,file=sys.stderr)
print("\n".join(sorted(out)))

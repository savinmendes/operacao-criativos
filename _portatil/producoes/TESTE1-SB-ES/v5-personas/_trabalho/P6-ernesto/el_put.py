import sys, requests
f, url, ct = sys.argv[1], sys.argv[2], sys.argv[3]
r = requests.put(url, data=open(f, "rb").read(), headers={"Content-Type": ct}); print(r.status_code, r.text[:200])

import sys, requests
f, url, ct = sys.argv[1], sys.argv[2], sys.argv[3]
r = requests.put(url, data=open(f, "rb").read(), headers={"content-type": ct, "x-amz-server-side-encryption": "AES256"})
print(r.status_code, f)

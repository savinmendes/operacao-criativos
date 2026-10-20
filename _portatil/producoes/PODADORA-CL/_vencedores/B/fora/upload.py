import json, sys, requests
# uso: python upload.py arquivo '<upload_url json>'
arq, desc = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
with open(arq, "rb") as f:
    files = list(desc["fields"].items())
    r = requests.post(desc["url"], data=desc["fields"], files={"file": (arq.split("\\")[-1], f, desc["fields"]["Content-Type"])})
print(r.status_code, r.text[:200])

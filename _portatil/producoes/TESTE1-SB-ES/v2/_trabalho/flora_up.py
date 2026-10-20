# -*- coding: utf-8 -*-
"""Envia arquivo para upload assinado do Flora (multipart POST). Uso: python flora_up.py arquivo resp.json"""
import json, sys, requests
arq, resp = sys.argv[1], sys.argv[2]
u = json.load(open(resp, encoding="utf-8"))
fields = dict(u["form_fields"])
with open(arq, "rb") as f:
    r = requests.post(u["url"], data=fields, files={u.get("file_field", "file"): (arq.split("\\")[-1].split("/")[-1], f, fields.get("Content-Type"))})
print(r.status_code, r.text[:300])

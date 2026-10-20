# -*- coding: utf-8 -*-
"""Upload compacto para o slot signed-url do Flora (só os campos que mudam).
  python flora_up.py arquivo key x-goog-date policy signature [content-type]"""
import sys

import requests

arq, key, date, policy, sig = sys.argv[1:6]
ct = sys.argv[6] if len(sys.argv) > 6 else ("video/mp4" if arq.lower().endswith(".mp4") else "image/jpeg")
cred_dia = date[:8]
campos = {"Content-Type": ct, "key": key, "x-goog-date": date,
          "x-goog-credential": f"vercel-app-prod@flora-prod-455015.iam.gserviceaccount.com/{cred_dia}/auto/storage/goog4_request",
          "x-goog-algorithm": "GOOG4-RSA-SHA256", "policy": policy, "x-goog-signature": sig}
with open(arq, "rb") as f:
    r = requests.post("https://storage.googleapis.com/flora-assets-prod/", data=campos,
                      files={"file": (arq.replace("/", "\\").split("\\")[-1], f, ct)}, timeout=600)
print(arq.split("\\")[-1], r.status_code, r.text[:300] if r.status_code >= 300 else "ok")

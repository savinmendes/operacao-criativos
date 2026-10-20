# -*- coding: utf-8 -*-
"""Gera lote p/ flora_upload.py reconstruindo a policy: python flora_lote.py saida.json arquivo|key|date|expiration|signature ..."""
import base64, json, sys
cred = "vercel-app-prod@flora-prod-455015.iam.gserviceaccount.com/{d}/auto/storage/goog4_request"
out = []
for a in sys.argv[2:]:
    arq, key, date, exp, sig = a.split("|")
    c = cred.format(d=date[:8])
    pol = {"conditions": [["content-length-range", 1, 367001600], {"Content-Type": "video/mp4"}, {"bucket": "flora-assets-prod"},
                          {"key": key}, {"x-goog-date": date}, {"x-goog-credential": c}, {"x-goog-algorithm": "GOOG4-RSA-SHA256"}],
           "expiration": exp}
    p = base64.b64encode(json.dumps(pol, separators=(",", ":")).encode()).decode()
    out.append({"arquivo": arq, "fields": {"Content-Type": "video/mp4", "key": key, "x-goog-date": date, "x-goog-credential": c,
                                           "x-goog-algorithm": "GOOG4-RSA-SHA256", "policy": p, "x-goog-signature": sig}})
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print(out[0]["fields"]["policy"][:60])

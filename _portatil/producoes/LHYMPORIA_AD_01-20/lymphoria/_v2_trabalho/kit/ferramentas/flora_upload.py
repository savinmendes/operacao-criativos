# -*- coding: utf-8 -*-
"""Envia arquivos locais para os slots "signed-url" que o flora_create_asset devolve.
  python flora_upload.py arquivo.mp4 descritor.json      # descritor = campo "upload_url" da resposta
  python flora_upload.py --lote lote.json                # [{"arquivo": "...", "fields": {...}}, ...]
Depois chame flora_complete_asset com cada asset_id."""
import json
import sys

import requests

URL = "https://storage.googleapis.com/flora-assets-prod/"


def envia(arq, campos, url=URL):
    with open(arq, "rb") as f:
        r = requests.post(url, data=campos, files={"file": (arq.replace("/", "\\").split("\\")[-1], f,
                                                            campos["Content-Type"])}, timeout=600)
    print(arq.split("\\")[-1], r.status_code, r.text[:300] if r.status_code >= 300 else "ok")


if sys.argv[1] == "--lote":
    for item in json.load(open(sys.argv[2], encoding="utf-8")):
        envia(item["arquivo"], item["fields"], item.get("url", URL))
else:
    d = json.load(open(sys.argv[2], encoding="utf-8"))
    envia(sys.argv[1], d["fields"], d["url"])

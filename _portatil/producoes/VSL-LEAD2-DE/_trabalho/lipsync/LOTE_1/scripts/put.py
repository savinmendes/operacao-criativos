# -*- coding: utf-8 -*-
"""Uso: python put.py up.json resposta_batch.json  -> faz os PUTs e grava/atualiza ../_tmp/assets.json {filename: asset_id}"""
import sys, json, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
AQ = Path(__file__).resolve().parent.parent
fs = json.load(open(sys.argv[1])); r = json.load(open(sys.argv[2])); it = r["items"]
assert len(fs) == len(it)
amap_p = AQ / "_tmp" / "assets.json"
amap = json.load(open(amap_p)) if amap_p.exists() else {}

def put(par):
    f, i = par; tid, kind = f["filename"].split("_"); src = AQ / "work" / tid / ("in.mp4" if kind == "in.mp4" else "de.mp3")
    assert src.stat().st_size == f["size_bytes"], src
    h = sum([["-H", f"{k}: {v}"] for k, v in i["upload_headers"].items()], [])
    code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", *h, "--data-binary", f"@{src}", i["upload_url"]],
                          capture_output=True, text=True).stdout
    return f["filename"], i["asset_id"], code

with ThreadPoolExecutor(6) as ex:
    for fn, aid, code in ex.map(put, zip(fs, it)):
        print(fn, code)
        if code == "200": amap[fn] = aid
json.dump(amap, open(amap_p, "w"), indent=1)
print("ok", sum(1 for f in fs if f["filename"] in amap), "/", len(fs))

# uso: python _baixar.py status.json  (aceita o json do status salvo pelo MCP) ; mapeia generation id -> nome
import json, sys, urllib.request, os
MAP = json.load(open("_ids.json", encoding="utf-8")) if os.path.exists("_ids.json") else {}
d = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(d, list): d = json.loads(d[0]["text"])
print("all_completed", d["all_completed"], "fail", d["has_failures"])
for g in d["generations"]:
    n = MAP.get(g["id"], g["id"]); print(n, g["status"], g.get("error_message", ""))
    if g["status"] == "completed":
        ext = ".png" if g["modality"] == "image" else ".mp4"
        out = n + ext if "/" in n else f"takes/{n}{ext}"
        if not os.path.exists(out): urllib.request.urlretrieve(g["content_url"], out)

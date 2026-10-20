import json, re, glob, html as H
ads = {}
def walk(o):
    if isinstance(o, dict):
        if "ad_archive_id" in o and "snapshot" in o:
            ads.setdefault(o["ad_archive_id"], o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
for f in sorted(glob.glob("raw/gql_*.txt")):
    for line in open(f, encoding="utf-8").read().splitlines():
        try: walk(json.loads(line))
        except Exception: pass
h = open("raw/html.txt", encoding="utf-8").read()
for m in re.finditer(r'<script type="application/json"[^>]*>(.*?)</script>', h, re.S):
    try: walk(json.loads(m.group(1)))
    except Exception: pass
ordem = json.load(open("raw/ordem_tela.json"))["ids"]
print(len(ads), "parsed;", sum(1 for i in ordem if i in ads), "of", len(ordem), "in order")
json.dump(ads, open("ads_raw.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
a = ads[ordem[0]]
print(json.dumps({k:v for k,v in a.items() if k!="snapshot"}, ensure_ascii=False)[:1500])
print(json.dumps(a["snapshot"], ensure_ascii=False)[:3000])
